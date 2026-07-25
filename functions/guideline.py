import numpy as np


class Guideline:

    def __init__(self):

        self.file = "checklist.txt"

        self.items = []


    def add_item(self, name, status):

        data = {
            "name": name,
            "status": status
        }

        self.items.append(data)



    def save(self):

        file = open(self.file, "w")

        for item in self.items:

            line = item["name"] + "," + str(item["status"])

            file.write(line + "\n")


        file.close()



    def load(self):

        self.items.clear()

        try:

            file = open(self.file, "r")


            for line in file:

                data = line.strip().split(",")


                if len(data) == 2:

                    item = {
                        "name": data[0],
                        "status": int(data[1])
                    }

                    self.items.append(item)


            file.close()


        except:

            pass



    def total_item(self):

        return len(self.items)



    def ready_item(self):

        count = 0


        for item in self.items:

            if item["status"] == 1:

                count += 1


        return count



    def statistics(self):

        status = []


        for item in self.items:

            status.append(item["status"])



        if len(status) == 0:

            return 0,0,0



        arr = np.array(status)


        total = len(arr)

        ready = np.sum(arr)

        percent = np.mean(arr)*100


        return total, ready, percent