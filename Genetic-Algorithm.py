import numpy as np
import matplotlib.pyplot as plt
import random


class GA:

    def __init__(self, computer=50, start=0, finish=9, individual=50, generation=1000, percent=2):

        self.computer = computer                                          # Количество компьютеров в сети
        self.start = start                                                # Номер отправителя
        self.finish = finish                                              # Номер получателя
        self.individual = individual                                      # Количество популяции
        self.generation = generation                                      # Количество поколений
        self.percent = percent                                            # Процент мутации
        self.path = np.zeros((self.computer, self.computer), int)              # Матрица пропускной способности каналов
        self.now_generation = np.zeros((self.individual, self.computer), int)  # Матрица хранящее текущее поколение

    def build_network(self):

        for i in range(self.computer):
            for j in range(i):
                if i != j:
                    self.path[i][j] = random.randint(self.computer-2, self.computer * 10)
                    self.path[j][i] = self.path[i][j]

        print(self.path)

    def first_generation(self):
        for i in range(self.individual):
            self.now_generation[i][0] = self.start
            self.now_generation[i][self.computer-1] = self.finish
            arr = np.setdiff1d(np.arange(0, self.computer), [self.start, self.finish])
            self.now_generation[i][1:self.computer-1] = np.random.choice(arr, self.computer - 2)

        print(self.now_generation)

    def sum_path(self, generation_sum):
        arr_sum = [0 for _ in range(self.individual)]
        for i in range(self.individual):
            for j in range(1, self.computer):
                arr_sum[i] += self.path[generation_sum[i][j-1]][generation_sum[i][j]]

        return arr_sum

    def tournament_selection(self, generation_select):

        good_individual = np.zeros((int(self.individual/2), self.computer), int)
        arr_sum = GA.sum_path(self, generation_select)

        for i in range(int(self.individual/2)):
            arr_number = np.random.choice(np.arange(0, self.individual), 10, replace=False)  # Выбераем 5 претендентоов
            min_value = self.computer*self.individual*10
            index_min_value = 0

            for j in range(len(arr_number)):
                if min_value > arr_sum[arr_number[j]]:
                    min_value = arr_sum[arr_number[j]]
                    index_min_value = arr_number[j]

            good_individual[i] = generation_select[index_min_value]

        return good_individual

    def element_crossing(self):
        good_generation = GA.tournament_selection(self, self.now_generation)
        new_generation = np.zeros((int(self.individual/2), self.computer), int)
        for i in range(1, int(self.individual / 2), 2):
            for j in range(self.computer):
                if j % 2 == 0:
                    new_generation[i][j] = good_generation[i - 1][j]
                    new_generation[i - 1][j] = good_generation[i][j]
                else:
                    new_generation[i - 1][j] = good_generation[i - 1][j]
                    new_generation[i][j] = good_generation[i][j]

        if int(self.individual/2) % 2 != 0:
            new_generation[int(self.individual/2)-1] = good_generation[random.randint(0, int(self.individual/2) - 1)]

        return new_generation

    def mutation(self, mutant_generation):
        try:
            for i in range(0, len(mutant_generation), int(100/self.percent)):
                arr = np.setdiff1d(np.arange(0, self.computer), [self.start, self.finish])
                mutant_generation[i][random.randint(1, self.computer-2)] = np.random.choice(arr, 1)
        except IndexError:
            ''''today without mutation'''
            pass

        return mutant_generation

    def run(self):
        GA.build_network(self)
        GA.first_generation(self)

        top_path = 0
        top_len = self.computer*self.individual*10
        last_generation = 0
        for i in range(self.generation):
            good = GA.tournament_selection(self, self.now_generation)
            new = GA.mutation(self, GA.element_crossing(self))
            self.now_generation[0:int(self.individual/2)] = good
            self.now_generation[int(self.individual/2):self.individual] = new
            arr_sum = GA.sum_path(self, self.now_generation)
            if top_len > min(arr_sum):

                top_path = arr_sum.index(min(arr_sum))
                top_len = min(arr_sum)
                last_generation = i

        plt.show()
        print(top_len)

        return self.now_generation[top_path]


a = GA()
print(a.run())
