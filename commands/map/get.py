class Dot(object):
    def __init__(self, x_cor, y_cor, place_desc, db, pl_id):
        self.db_helper = db
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.place_desc = place_desc
        self.paths = self.get_picture(pl_id)

    def get_picture(self, pl_id):
        sql = f" select pip.path_value from place_path plp" \
              f" join picture_path pip on pip.path_id = plp.path_id and plp.pl_id={pl_id}"
        return self.db_helper.query(sql)


class MapXY(object):
    def __init__(self, db_helper, country):
        self.country = country
        self.x_location = None
        self.y_location = None
        self.db_helper = db_helper
        self.dots = self.get_dot()

    def search_optimal_picture(self):
        pass

    def check_country(self):
        sql = f" select cntr_id, x_location, y_location from country where cntr_name = '{self.country}'"
        if self.db_helper.query(sql) is not None:
            self.x_location = self.db_helper.query(sql)[0][1]
            self.y_location = self.db_helper.query(sql)[0][2]
            return self.db_helper.query(sql)[0][0]
        print(f"Country {self.country} doesn't exist")
        exit(1)

    def get_dot(self):
        dots = []
        cntr_id = self.check_country()
        sql = f" SELECT pi.pl_id, pi.x_coor, pi.y_coor, pi.place_desc, c.cntr_name from place_info pi" \
              f" join country_place cp on cp.pl_id=pi.pl_id" \
              f" join country c on c.cntr_id=cp.cntr_id and c.cntr_id = {cntr_id}"
        place_desc = self.db_helper.query(sql)
        for place in place_desc:
            print(place)
            dot = Dot(
                x_cor=place[1],
                y_cor=place[2],
                place_desc=place[3],
                db=self.db_helper,
                pl_id=place[0]
            )
            dots.append(dot)
        return dots