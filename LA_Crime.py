#Which hour has the highest frequency of crimes? Store as an integer variable called peak_crime_hour.
peak_crime_hour = crimes["TIME OCC"].value_counts(normalize=True).idxmax()
print(peak_crime_hour)

#Which area has the largest frequency of night crimes (crimes committed between 10pm and 3:59am)? Save as a string variable called peak_night_crime_location.

#Define night hours
after_midnight = crimes[(crimes["TIME OCC"] <= "0359") & (crimes["TIME OCC"] >= "0000")]
before_midnight = crimes[(crimes["TIME OCC"] >= "2200") & (crimes["TIME OCC"] <= "2359")]

#Combine crimes occurring before and after midnight into a single DataFrame & find the area with the highest proportion of night crimes
night_crime = pd.concat([before_midnight, after_midnight])
peak_night_crime_location = night_crime["AREA NAME"].value_counts(normalize=True).idxmax()
print(peak_night_crime_location)

#Identify the number of crimes committed against victims of different age groups. Save as a pandas Series called victim_ages, with age group labels "0-17", "18-25", "26-34", "35-44", "45-54", "55-64", and "65+" as the index and the frequency of crimes as the values.

# Define the age groups
age_bins = [0, 17, 25, 34, 44, 54, 64, float('inf')]
age_labels = ["0-17", "18-25", "26-34", "35-44", "45-54", "55-64", "65+"]

# Categorize victim ages into age groups
crimes['Age Group'] = pd.cut(crimes['Vict Age'], bins=age_bins, labels=age_labels)

# Count the number of crimes in each age group
victim_ages = crimes['Age Group'].value_counts()

# Display the results
print(victim_ages)
