
class ManageMapXY(object):
    def __init__(self, db_helper):
        self.db_helper = db_helper

    def delete_pick(self):
        pass

    def add_place(self):
        sql = f" select cntr_id, cntr_name from country"
        cntr = self.db_helper.query(sql)
        if cntr is None:
            print("There are no countries in the database yet. Want to add?")
            while True:
                ans = input("YES/NO ")
                if ans.lower() == "no":
                    exit(1)
                if ans.lower() == "yes":
                    x_location = float(input("x_location: "))
                    y_location = float(input("y_location: "))
                    cntr_name = input("Name: ")
                    sql = f"insert into country (x_location, y_location, cntr_name) " \
                          f"values ({x_location}, {y_location}, '{cntr_name}'"
                    self.db_helper.query(sql)
                    self.db_helper.commit_conn()
                    break
        cntr_id_list = [ c[0] for c in cntr]
        while True:
            for c in cntr:
                print(f"{c[1]}. Enter {c[0]}")
            cntr_id = int(input("If you want add another country, enter 0. Enter: "))
            if cntr_id in cntr_id_list:
                break
            if cntr_id == 0:
                exit(1)
            print("Wrong number of country!!")
        x_location = input("x_location: ")
        y_location = input("y_location: ")
        place_desc = input("Description: ")
        sql = f"insert into place_info (x_coor, y_coor, place_desc) " \
              f"values ('{x_location}', '{y_location}', '{place_desc}') RETURNING pl_id"
        pl_id = self.db_helper.query(sql)[0][0]
        sql = f"insert into country_place (pl_id, cntr_id) " \
              f"values ({pl_id}, {cntr_id})"
        self.db_helper.query(sql)
        self.db_helper.commit_conn()

    def add_pick(self):
        x_coor = input("x_location: ")
        y_coor = input("y_location: ")
        sql = f" select pl_id from place_info where x_coor='{x_coor}' and y_coor='{y_coor}'"
        print(sql)
        pl_id = self.db_helper.query(sql)
        if pl_id is None:
            print("Dot doesn't exist")
            exit(1)
        path = input("Name: ")
        sql = f"insert into picture_path (path_value) " \
              f"values ('{path}') RETURNING path_id"
        path_id = self.db_helper.query(sql)[0][0]
        sql = f"insert into place_path (pl_id, path_id) " \
              f"values ({pl_id[0][0]}, {path_id})"
        self.db_helper.query(sql)
        self.db_helper.commit_conn()

    def add_country(self):
        x_location = input("x_location: ")
        y_location = input("y_location: ")
        cntr_name = input("Name: ")
        sql = f" select cntr_id from country where x_location='{x_location}' and y_location='{y_location}'"
        if len(self.db_helper.query(sql)) != 0:
            print("Country with coordinates already exist")

        sql = f" select cntr_id from country where cntr_name='{cntr_name}'"
        if len(self.db_helper.query(sql)) != 0:
            print(f"Country with name {cntr_name} already exist")
            exit(1)
        sql = f"insert into country (x_location, y_location, cntr_name) " \
              f"values ('{x_location}', '{y_location}', '{cntr_name}')"
        self.db_helper.query(sql)
        self.db_helper.commit_conn()

    def run(self, args):
        if args.picture:
            self.add_pick()
        if args.dot:
            self.add_place()
        if args.country:
            self.add_country()