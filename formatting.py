#reformat numbers in nltk soup
length = len(numbers)
f_numbers =[]
for i in range(0,length):
    if len(numbers[i]) == 10:
        f_numbers.append("("+numbers[i][:3]+") "+numbers[i][3:6]+"-"+numbers[i][6:])
    else:
        f_numbers.append(numbers[i][:3]+"-"+numbers[i][3:])

#cast df email fields to lowercase for better match
df['Email 1'] = df['Email 1'].str.lower()
df['Email 2'] = df['Email 2'].str.lower()

#filter spaces and special characters cast to lower for proper names
df['filter'] = df['Full Name'].str.lower().astype(str).map(lambda x: re.sub(r'\W+', '', x))

length = len(emails)
for i in range(0,length):
    emails[i] = emails[i].lower()
    
#save matching emails into an array of dataframes
array = []
for e in emails:
    print(e)
    array.append(df[df.apply(lambda r: r.str.contains(e, case=False).any(), axis=1)])

#save matching numbers into an array of dataframes
array2 = []
for i in numbers:
    print(i)
    array2.append(df[df.apply(lambda r: r.str.contains(i, case=False).any(), axis=1)])

#combine the email arrays into a single dataframe
length = len(array)
for i in range(0,length):
    print(i)
    array[0] = pd.concat([array[0],array[i+1]], sort = False)

#do the same for number array
length = len(array2)
for i in range(0,length):
    print(i)
    array2[0] = pd.concat([array2[0],array2[i+1]], sort = False)

results = pd.concat([array[0],array2[0]], sort = False)
    
