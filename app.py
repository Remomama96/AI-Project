 
import pickle
import streamlit as st

 
# loading the trained model
pickle_in = open('NV.pkl', 'rb') 
classifier = pickle.load(pickle_in)
 
@st.cache()
  
# defining the function which will make the prediction using the data which the user inputs 
def prediction(Credit_Card_Exceed_Months, Employment_Type,More_Than_One_Products,Number_of_Dependents,Years_to_Financial_Freedom,Number_of_Credit_Card_Facility,Number_of_Loan_to_Approve,Property_Type,Years_for_Property_to_Completion,State,Monthly_Salary,Total_Sum_of_Loan,Score,monthly_loan_payment,Loan_Tenure_Month):   
 
    # Pre-processing user input    
    if Employment_Type == "Fresh Graduate":
        Employment_Type = 0
    elif Employment_Type == "Self Employed":
        Employment_Type = 1 
    elif Employment_Type == "Unknown":
        Employment_Type = 2           
    elif Employment_Type == "Employee":
        Employment_Type = 3        
    elif Employment_Type == "Employer":
        Employment_Type = 4   
    else:
        Employment_Type = 5
 
    if More_Than_One_Products == "No":
        More_Than_One_Products = 0
    else:
        More_Than_One_Products = 1
  
        
    if Property_Type == "Unknown":
        Property_Type = 0
    elif Property_Type == "Bungalow":  
        Property_Type = 1        
    elif Property_Type == "Condominium":  
        Property_Type = 2
    elif Property_Type == "Terrace":  
        Property_Type = 3     
    else:
        Property_Type = 4
    
    if State == "Johor":
        State = 0
    elif State == "Kedah":
        State = 3
    elif State == "Kuala Lumpur":  
        State = 4
    elif State == "N.Sembilan":
        State = 6
    elif State == "Penang":
        State = 8
    elif State == "Sabah":
        State = 11
    elif State == "Sarawak":
        State = 12
    elif State == "Selangor":
        State = 13
    else:
        State = 14   
 
    # Making predictions 
    prediction = classifier.predict( 
        [[Credit_Card_Exceed_Months, Employment_Type,More_Than_One_Products,Number_of_Dependents,Years_to_Financial_Freedom,Number_of_Credit_Card_Facility,Number_of_Loan_to_Approve,Property_Type,Years_for_Property_to_Completion,State,Monthly_Salary,Total_Sum_of_Loan,Score,monthly_loan_payment,Loan_Tenure_Month]])
     
    if prediction == 0:
        pred = 'Rejected'
    else:
        pred = 'Approved'
    return pred
      
  
# this is the main function in which we define our webpage  
def main():       
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:yellow;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Streamlit Loan Prediction ML App</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    # following lines create boxes in which user can enter data required to make prediction 
    Employment_Type = st.selectbox('Employment Type',("Fresh Graduate","Self Employed","Unknown","Employee","Employer","Government"))
    More_Than_One_Products = st.selectbox('More Than One Products',("No","Yes"))
    Property_Type = st.selectbox('Property Type',("Unknown","Bungalow","Condominium","Terrace","Flat"))
    State = st.selectbox('State',("Johor","Kedah","Kuala Lumpur","N.Sembilan","Penang","Sabah","Sarawak","Selangor","Terengganu"))
    Credit_Card_Exceed_Months = st.number_input("Credit Card Exceed Months")
    Number_of_Dependents = st.number_input("Number of Dependents")
    Years_to_Financial_Freedom = st.number_input("Years to Financial Freedom")
    Number_of_Credit_Card_Facility = st.number_input("Number of Credit Card Facility")
    Number_of_Loan_to_Approve = st.number_input("Number of Loan to Approve")
    Years_for_Property_to_Completion = st.number_input("Years for Property to Completion") 
    Monthly_Salary = st.number_input("Monthly Salary")
    Total_Sum_of_Loan = st.number_input(" Total Sum of Loan")
    Score = st.number_input("Score")
    monthly_loan_payment = st.number_input("Monthly Loan Payment")
    Loan_Tenure_Month = st.number_input("Loan Tenure Month")
    result =""
      
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(Credit_Card_Exceed_Months, Employment_Type,More_Than_One_Products,Number_of_Dependents,Years_to_Financial_Freedom,Number_of_Credit_Card_Facility,Number_of_Loan_to_Approve,Property_Type,Years_for_Property_to_Completion,State,Monthly_Salary,Total_Sum_of_Loan,Score,monthly_loan_payment,Loan_Tenure_Month) 
        st.success('Your loan is {}'.format(result))
        print(monthly_loan_payment*Loan_Tenure_Month)
     
if __name__=='__main__': 
    main()
