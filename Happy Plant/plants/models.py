from django.db import models
from users.models import User

class Plant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    age = models.IntegerField()
    last_watered = models.DateTimeField(auto_now_add=True)

    # species წესით ჯობია იყოს choises
    # მაგრამ მაგისთვის გვჭირდება ბაზა მცენარეების სახეობებზე

    # არ მომწონს age, მაგრამ არ ვიცი როგორ გავაკეთო
    # გვინდა, რომ იუზერმა შეიყვანოს რამდენი დღისაა ან კვირის
    # ამის შემდეგ ყოველდღიურად +1 დღე იყოს და სადმე გამოჩნდეს 

    def __str__(self):
        return f"{self.name} ({self.species})"

