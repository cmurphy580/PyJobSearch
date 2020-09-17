class Listing():
    def __init__(self, title="Engineer", company="In Description",
                 salary="Not Listed", location="US", date="24 hrs",
                 logo="https://image.flaticon.com/icons/svg/306/306424.svg", link="None"):
        self.title = title
        self.company = company
        self.salary = salary
        self.location = location
        self.date = date
        self.logo = logo
        self.link = link
        self.description = ""
        self.favorite = False

    def __eq__(self, other):
        return True if self.title == other["title"] and self.company == other["company"] or self.title == other["title"] and self.link == other["link"] else False

    def to_dict(self):
        return {"title": self.title, "company": self.company,
                "salary": self.salary, "location": self.location,
                "date": self.date, "logo": self.logo, "link": self.link,
                "favorite": self.favorite}
