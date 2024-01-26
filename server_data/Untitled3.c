#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

sem_t mutex;

void* P(void* arg) {
    int number = *(int*)arg, i;

    for ( i = 0; i < 2; ++i) {
        sem_wait(&mutex);

        // Critical Section
        printf("%d\n", number);
        printf("%d\n", number + 1);

        sem_post(&mutex);
    }

    return NULL;
}

int main() {
    pthread_t thread1, thread2, thread3;

    sem_init(&mutex, 0, 1);  // Initialize semaphore with initial value 1

    int num1 = 1, num2 = 3, num3 = 5;

    pthread_create(&thread1, NULL, P, &num1);
    pthread_create(&thread2, NULL, P, &num2);
    pthread_create(&thread3, NULL, P, &num3);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    pthread_join(thread3, NULL);

    sem_destroy(&mutex);

    return 0;
}

