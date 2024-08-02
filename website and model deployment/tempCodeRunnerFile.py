import pandas as pd
df = pd.read_excel("C:/Users/sivar/OneDrive/Desktop/Mini Project Chatbot/model_deployment/dataset_chatbot.xlsx")
df.head()
col_to_drop=['S NO','APPLN NO','NAME OF THE CANDIDATE','DOB','RANK','ALLOTTED\nCATEGORY']
df.drop(columns=col_to_drop, inplace=True)
df.describe()
df['COMMUNI\nTY'] = df['COMMUNI\nTY'].str.replace('COMMUNI\nTY', '')
df['COMMUNI\nTY'].unique()
df.replace('', pd.NA, inplace=True)
df.dropna(inplace=True)
df['COMMUNI\nTY'].unique()
df.sort_values(by='COMMUNI\nTY').describe()
co_range = df.groupby(['COLLEGE\nCODE', 'COMMUNI\nTY', 'BRANCH\nCODE']).agg({'AGGR\nMARK': ['min', 'max']})
def predict_colleges_and_branches(agg_marks, community):
    # Convert AGGR\nMARK to float for comparison
    agg_marks = float(agg_marks)
    
    # Filter the DataFrame based on the provided community
    filtered_df = co_range.loc[(slice(None), community), :]
    
    # Initialize a list to store matching colleges and branches
    matches = []
    
    # Iterate over the filtered DataFrame
    for index, row in filtered_df.iterrows():
        college_code = index[0]
        branch_code = index[2]
        min_cutoff = float(row[('AGGR\nMARK', 'min')])  # Convert to float
        max_cutoff = float(row[('AGGR\nMARK', 'max')])  # Convert to float
        
        # Check if the aggregate marks fall within the range
        if min_cutoff <= agg_marks <= max_cutoff:
            matches.append((college_code, branch_code))
    
    # Check if any matches were found
    if matches:
        return matches
    else:
        return ["No colleges found for the given aggregate marks and community."]

agg_marks_input = input("Enter your aggregate marks: ")
community_input = input("Enter your community: ")

result = predict_colleges_and_branches(agg_marks_input, community_input)
for prediction in result:
    print("Predicted College Code:", prediction[0])
    print("Predicted Branch Code:", prediction[1])
    