import math as m


class perceptron:
    def __init__(self, bits_to_index, history_length):
        self.bits_to_index = bits_to_index
        self.history_length = history_length
        self.size_of_weights_table = 2**bits_to_index
        self.y_out = 0
        self.threshold = m.floor((1.93 * history_length) + 14)

        self.GH_reg = [0 for i in range(history_length)]
        self.GH_reg[0] = 1  # Bias input

        self.weights_table = [
            self.GH_reg for i in range(self.size_of_weights_table)
            ]

        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\tPerceptron")

        print(
            "\tTamaño de Tabla de Historia:\t\t" +
            str(self.history_length)
            )
        print(
            "\tTamaño de Tabla de pesos:   \t\t" +
            str(self.size_of_weights_table)
            )

    def print_stats(self):
        print("Resultados de la simulación")
        print(
            "\t# branches:\t\t\t\t\t\t" +
            str(self.total_predictions)
            )
        print(
            "\t# branches tomados predichos correctamente:\t\t" +
            str(self.total_taken_pred_taken)
            )
        print(
            "\t# branches tomados predichos incorrectamente:\t\t" +
            str(self.total_taken_pred_not_taken)
            )
        print(
            "\t# branches no tomados predichos correctamente:\t\t" +
            str(self.total_not_taken_pred_not_taken)
            )
        print(
            "\t# branches no tomados predichos incorrectamente:\t" +
            str(self.total_not_taken_pred_taken)
            )
        perc_correct = (100*(self.total_taken_pred_taken +
                        self.total_not_taken_pred_not_taken) /
                        self.total_predictions
                        )
        formatted_perc = "{:.3f}".format(perc_correct)
        print(
            "\t% predicciones correctas:\t\t\t\t" +
            str(formatted_perc)+"%"
            )

    def predict(self, PC):
        PC_index = int(PC) % self.size_of_weights_table
        x = self.GH_reg
        w = self.weights_table[PC_index]

        self.y_out = sum([
            xi*wi for xi, wi in zip(x, w)
            ])

        if self.y_out <= 0:
            return "N"
        else:
            return "T"

    def update(self, PC, result, prediction):
        if result == "N":
            t = -1
        else:
            t = 1

        miss = True
        if result == prediction:
            hit = False
        else:
            miss = True

        PC_index = int(PC) % self.size_of_weights_table
        x = self.GH_reg
        w = self.weights_table[PC_index]

        # ==== UPDATING THE WEIGHTS USED === #

        temp_w = w
        if ((miss) or
                (abs(self.y_out) <= self.threshold)):

            temp_w = [
                (wi + (t*xi)) for xi, wi in zip(x, w)
                ]

        self.weights_table[PC_index] = temp_w

        # ==== UPDATING HISTORY REGISTER ==== #

        if result == "T":
            self.GH_reg = x[1:] + [1]
        else:
            self.GH_reg = x[1:] + [-1]

        self.GH_reg[0] = 1  # input bias

        # ==== UPDATE STATS ==== #

        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1

        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1

        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1

        else:
            self.total_not_taken_pred_taken += 1

        self.total_predictions += 1
