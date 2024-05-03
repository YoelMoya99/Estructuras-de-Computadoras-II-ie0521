class pshared:
    def __init__(self,bits_to_index, pattern_table_size):
        #Escriba aquí el init de la clase
        self.bits_to_index = bits_to_index
        self.size_of_history_table = 2**bits_to_index
        self.size_of_pattern_table = 2**pattern_table_size
        self.despl_reg_size = pattern_table_size

        base_reg = ""
        for i in range(pattern_table_size):
            base_reg += "0"

        self.history_table = [
            base_reg for i in range(self.size_of_history_table)
            ]

        self.pattern_table = [
                0 for i in range(self.size_of_pattern_table)
                ]

        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\tP-Shared")

        print(
            "\tTamaño de Tabla de Historia:\t\t" +
            str(self.size_of_history_table)
            )
        print(
            "\tTamaño de Tabla de Patrones:\t\t" +
            str(self.size_of_pattern_table)
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
        #Escriba aquí el código para predecir
        #La siguiente línea es solo para que funcione la prueba
        #Quítela para implementar su código
        PC_index = int(PC) % self.size_of_history_table
        Ptrn_index = int(self.history_table[PC_index], 2)
        Counter = self.pattern_table[Ptrn_index]

        if Counter in [0, 1]:
            return "N"
        else:
            return "T"
  

    def update(self, PC, result, prediction):
        #Escriba aquí el código para actualizar
        #La siguiente línea es solo para que funcione la prueba
        #Quítela para implementar su código
        PC_index = int(PC) % self.size_of_history_table
        Str_Ptrn_index = self.history_table[PC_index]
        Ptrn_index = int(Str_Ptrn_index, 2)
        Counter = self.pattern_table[Ptrn_index]

        # ==== UPDATING THE COUNTER IN PATTERN TABLE ==== # 

        if Counter == 0 and result == "N":
            pass
        elif Counter != 0 and result == "N":
            Counter -= 1
        elif Counter == 3 and result == "T":
            pass
        else:
            Counter += 1

        self.pattern_table[Ptrn_index] = Counter  # new counter

        # ==== UPDATING THE HISTORY TABLE ==== #

        if result == "T":
            self.history_table[PC_index] = (
                    Str_Ptrn_index[-self.despl_reg_size+1:] + "1"
                    )
        else:
            self.history_table[PC_index] = (
                    Str_Ptrn_index[-self.despl_reg_size+1:] + "0"
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


