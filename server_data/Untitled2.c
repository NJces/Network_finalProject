#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

sem_t sem1, sem2, sem3;

void* P1(void* arg) {
    sem_wait(&sem1);
    printf("1\n");
    printf("2\n");
    sem_post(&sem2);

    return NULL;
}

void* P2(void* arg) {
    sem_wait(&sem2);
    printf("3\n");
    
    printf("4\n");
    sem_post(&sem3);

    return NULL;
}

void* P3(void* arg) {
    sem_wait(&sem3);
    printf("5\n");
    printf("6\n");
    sem_post(&sem1);

    return NULL;
}

int main() {
    pthread_t thread1, thread2, thread3;

    sem_init(&sem1, 0, 1);
    sem_init(&sem2, 0, 0);
    sem_init(&sem3, 0, 0);

    pthread_create(&thread1, NULL, P1, NULL);
    pthread_create(&thread2, NULL, P2, NULL);
    pthread_create(&thread3, NULL, P3, NULL);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    pthread_join(thread3, NULL);

    sem_destroy(&sem1);
    sem_destroy(&sem2);
    sem_destroy(&sem3);

    return 0;
}

