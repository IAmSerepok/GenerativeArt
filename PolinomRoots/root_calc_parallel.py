import numpy as np
from multiprocessing import Pool, cpu_count, Manager
import time, os
import queue as pyqueue
import traceback


def find_roots_vectorized(batch_size):
    try:
        # Генерация всех alpha1 и alpha2 сразу
        alpha1 = np.random.uniform(0, 2 * np.pi, batch_size)
        alpha2 = np.random.uniform(0, 2 * np.pi, batch_size)
        
        t1 = np.cos(alpha1) + 1j * np.sin(alpha1)
        t2 = np.cos(alpha2) + 1j * np.sin(alpha2)
        
        results = []
        
        for i in range(batch_size):
            # Извлекаем скалярные значения для текущей итерации
            t1_i = t1[i]
            t2_i = t2[i]
            
            coeffs = np.array([
                -1j, 1j, -1, -1j, 1j, 1j, 1, 1j, -1j, 
                t1_i ** 5 * (11.5-20.9j) + t1_i ** 4 * (14.9+3.59j) + 
                t1_i ** 3 * (4.5+8.04j) + t1_i ** 2 * (6.65+5.2j) + 
                t1_i * (-3.97+3.18j) + 2.67 - 0.0536j, 
                t2_i * (-0.553+0.999j) - 1.14 + 1.6j, 
                1
            ], dtype=complex)
            
            roots = np.roots(coeffs)
            
            for root_idx, root in enumerate(roots):
                results.append(f"{root.real:.6f},{root.imag:.6f},{root_idx}")
        
        return results
    except Exception as e:
        print(f"Ошибка в find_roots_vectorized: {e}")
        traceback.print_exc()
        return []


def worker_process(args, queue):
    try:
        batch_size, num_batches, worker_id = args
        np.random.seed(int(time.time() * 1000) % 2 ** 32 + os.getpid() + worker_id)
        
        for batch_num in range(num_batches):
            result = find_roots_vectorized(batch_size)
            if result:
                queue.put(result)
        
        queue.put(None)  # Сигнал завершения
        
    except Exception as e:
        print(f"Ошибка в worker_process {args[2]}: {e}")
        traceback.print_exc()
        queue.put(None)


def parallel_vectorized(num_samples=5_000_000, batch_size=100):
    num_workers = cpu_count()
    num_batches = num_samples // batch_size
    batches_per_worker = num_batches // num_workers
    
    with Manager() as manager:
        queue = manager.Queue() 
        
        # Запускаем процессы
        pool = Pool(processes=num_workers)
        async_results = []
        
        for i in range(num_workers):
            if i == num_workers - 1:
                worker_batches = num_batches - i * batches_per_worker
            else:
                worker_batches = batches_per_worker
            
            if worker_batches > 0:
                args = (batch_size, worker_batches, i)
                async_result = pool.apply_async(worker_process, args=(args, queue))
                async_results.append(async_result)
        
        # Пишем в файл
        with open('data.csv', 'w') as f:
            start_time = time.time()
            completed_workers = 0
            total_written = 0
            N = 11  # корней на полином
            
            while completed_workers < len(async_results):
                try:
                    # Увеличиваем timeout до 30 секунд
                    batch_result = queue.get(timeout=30)
                    
                    if batch_result is None:
                        completed_workers += 1
                    else:
                        # Записываем батч
                        batch_lines = '\n'.join(batch_result)
                        f.write(batch_lines + '\n')
                        
                        total_written += len(batch_result)
                        
                        # Прогресс
                        if total_written % (batch_size * 10) == 0:
                            samples_done = total_written // N
                            if samples_done > 0:
                                print(f"Обработано: {samples_done:,}/{num_samples:,} полиномов "
                                      f"({samples_done/num_samples*100:.1f}%)")
                
                except pyqueue.Empty:
                    # Проверяем, все ли воркеры еще работают
                    all_done = all(async_result.ready() for async_result in async_results)
                    if all_done:
                        print("Все воркеры завершились, но сигналы не получены")
                        break
                    else:
                        print(f"Таймаут очереди, но воркеры еще работают... "
                              f"Размер очереди: {queue.qsize()}")
                        # Продолжаем ждать
                        continue
                except Exception as e:
                    print(f"Ошибка при записи: {e}")
                    break
        
        # Ждем завершения всех воркеров
        pool.close()
        print("Ожидание завершения пула процессов...")
        pool.join()
        print("Пул процессов завершен")
    
    # Проверяем результаты
    for i, async_result in enumerate(async_results):
        try:
            async_result.get(timeout=1)
        except Exception as e:
            print(f"Воркер {i} завершился с ошибкой: {e}")
    
    total_time = time.time() - start_time
    print(f"Общее время: {total_time/60:.2f} минут")


if __name__ == '__main__':
    parallel_vectorized(num_samples=5_000_000, batch_size=100)
