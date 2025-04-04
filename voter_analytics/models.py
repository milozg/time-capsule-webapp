from django.db import models

# Create your models here.

class Voter(models.Model):
    '''
    A model class to store the information of a voter.

    Voter ID Number, Last Name, First Name, Residential Address - Street Number,
    Residential Address - Street Name, Residential Address - Apartment Number,
    Residential Address - Zip Code, Date of Birth, Date of Registration,
    Party Affiliation, Precinct Number, v20state, v21town, v21primary
    v22general, v23town, voter_score
    '''

    # Identification
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.TextField()
    dob = models.DateField()

    # Voter Information
    dor = models.DateField()
    affiliation = models.CharField(max_length=1)
    precinct = models.TextField()

    #Voter History
    v20state = models.TextField()
    v21town = models.TextField()
    v21primary = models.TextField()
    v22general = models.TextField()
    v23town = models.TextField()
    voter_score = models.IntegerField()

    def get_address(self):
        '''return a string of the address of this voter'''
        address = "https://www.google.com/maps?q="
        address += self.street_number + "+"
        address += self.street_name + ",+"
        address += "Newton+MA,+"
        address += self.zip_code

        return address


    def __str__(self):
        '''Return a string representation of the voter model'''
        return f'{self.first_name} {self.last_name}'

def load_data():
    '''A function to load the data of the CSV file into the django database.'''

    Voter.objects.all().delete()

    filename = '/Users/mish/Desktop/newton_voters.csv'
    file = open(filename)
    file.readline()

    for line in file:
        fields = line.strip().split(',')
        
        voter = Voter(
            # Identification
            last_name = fields[1],
            first_name = fields[2],
            street_number = fields[3],
            street_name = fields[4],
            zip_code = fields[6],
            dob = fields[7],

            # Voter Information
            dor = fields[8],
            affiliation = fields[9],
            precinct = fields[10],

            # Voter History
            v20state = fields[11],
            v21town = fields[12],
            v21primary = fields[13],
            v22general = fields[14],
            v23town = fields[15],
            voter_score = fields[16],
        )
        # Appartment number could be blank
        if fields[5] != '':
            voter.apartment_number = fields[5]
        
        voter.save()
    
    print(f'Done. Created {len(Voter.objects.all())} Voters.')
