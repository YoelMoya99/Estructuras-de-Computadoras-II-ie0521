class ie0521_bp:
    def __init__(self):
        self.bits_to_index = 4
        self.size_of_history_table = 2**4
        self.global_history_size = self.bits_to_index

        self.GH_reg = ""
        for i in range(self.bits_to_index):
            self.GH_reg += "0"

        self.history_table = [
            0 for i in range(self.size_of_history_table)
            ]

        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t Trendlines")
        print("\tBits para indexar:\t\t\t ", self.bits_to_index)
        print(
            "\tTamaño de la tabla:\t\t\t", self.size_of_history_table
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
        perc_correct = (100 * (self.total_taken_pred_taken +
                        self.total_not_taken_pred_not_taken) /
                        self.total_predictions
                        )
        formatted_perc = "{:.3f}".format(perc_correct)
        print(
            "\t% predicciones correctas:\t\t\t\t" +
            str(formatted_perc)+"%"
            )

    def predict(self, PC):
        PC_index = int(PC) % self.size_of_history_table
        Counter = self.history_table[PC_index]

        if Counter == 0:
            return "N"
        elif Counter == 3:
            return "T"
        else:
            if sum([int(i) for i in self.GH_reg]) > 8:
                return "T"
            else:
                return "N"

    def update(self, PC, result, prediction):

        PC_index = int(PC) % self.size_of_history_table
        Counter = self.history_table[PC_index]

        # ==== UPDATING THE COUNTER IN HISTORY TABLE ==== #

        if Counter == 0 and result == "N":
            pass
        elif Counter != 0 and result == "N":
            Counter -= 1
        elif Counter == 3 and result == "T":
            pass
        else:
            Counter += 1

        # ==== UPDATING GLOBAL HISTORY REGISTER ==== #

        if result == "T":
            self.GH_reg = (
                    self.GH_reg[-self.bits_to_index+1:] + "1"
                    )
        else:
            self.GH_reg = (
                    self.GH_reg[-self.bits_to_index+1:] + "0"
                    )

        # ==== UPDATE STATS === #

        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1

        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1

        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1

        else:
            self.total_not_taken_pred_taken += 1

        self.total_predictions += 1
