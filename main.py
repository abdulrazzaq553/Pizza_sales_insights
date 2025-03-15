import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
data=pd.read_csv('pizza_sales.csv')


st.set_page_config(page_title="Pizza Sales Insights", layout="wide")  
st.title("🍕 Pizza Sales Insights Dashboard")  


data['order_date']=pd.to_datetime(data['order_date'], format='%d-%m-%Y')
data['month']=data['order_date'].dt.strftime('%b')

Month=data['month'].unique().tolist()
Month.insert(0,'Overall')
select_month=st.selectbox('Choose Month',Month)


col1,col2,col3,col4,col5=st.columns(5)
with col1:

   if select_month=='Overall':
       Total=data['total_price'].sum()
       st.metric('Total_Value:',Total)
   else:
        data=data[data['month']==select_month]
        Total=data['total_price'].sum()
        Total=round(Total,3)
        st.metric('Total_Value:',Total)


avg_order_value=(data['total_price'].sum())/(data['order_id'].drop_duplicates().count())
with col2:
    if select_month=='Overall':
       
       avg_order_value=(data['total_price'].sum())/(data['order_id'].drop_duplicates().count())
       st.metric('Average Order Value:',round(avg_order_value,3))
    else:
         data=data[data['month']==select_month]
          
         avg_order_value=(data['total_price'].sum())/(data['order_id'].drop_duplicates().count())
         st.metric('Average Order Value:',round(avg_order_value,3))


with col3:

 
    if select_month=='Overall':
       
       total_pizza_sold=data['quantity'].sum()  
       st.metric('Total_Pizza_sold:',round(total_pizza_sold,3))
    else:
         data=data[data['month']==select_month]
         total_pizza_sold=data['quantity'].sum()  
         st.metric('Total_Pizza_sold:',round(total_pizza_sold,3)) 
with col4:
   
     if select_month=='Overall':
       
       count=data['order_id'].drop_duplicates().count()
       st.metric('Total_order:',round(count,3))
     else:
         data=data[data['month']==select_month]
         count=data['order_id'].drop_duplicates().count()
         st.metric('Total_Order:',round(count,3)) 
with col5:
    if select_month=='Overall':
       
       avg_pizza=data['quantity'].sum()/data['order_id'].drop_duplicates().count()
       st.metric('Avg_pizza_per_order:',round(avg_pizza,3))
    else:
         data=data[data['month']==select_month]
         avg_pizza=data['quantity'].sum()/data['order_id'].drop_duplicates().count()
         st.metric('Avg_pizza_per_order:',round(avg_pizza,3))
    
col6,col7=st.columns(2)
data['Day']=data['order_date'].dt.strftime('%a')

with col6: 
    if select_month=='Overall':
          
        plot=data.groupby('Day',as_index=False)['order_id'].count().sort_values(by='order_id',ascending=False)
        st.subheader('Order Count by Day')
        fig, ax = plt.subplots(figsize=(6, 4))
        bars=ax.bar(plot['Day'], plot['order_id'], color='brown')
        for bar in bars:
                 height = bar.get_height()
                 ax.text(bar.get_x() + bar.get_width()/2, height, f'{height}', 
            ha='center', va='bottom', fontsize=10, fontweight='bold')
# Labels and Title
        ax.set_xlabel('Day of the Week')  

        ax.set_ylabel('Order Count')
        ax.set_title('Total Orders per Day')
        st.pyplot(fig)

    else:
        data=data[data['month']==select_month]
        plot=data.groupby('Day',as_index=False)['order_id'].count().sort_values(by='order_id',ascending=False)
        st.subheader('Order Count by Day')

        fig, ax = plt.subplots(figsize=(6, 4))
        bars=ax.bar(plot['Day'], plot['order_id'], color='brown')
        for bar in bars:
                 height = bar.get_height()
                 ax.text(bar.get_x() + bar.get_width()/2, height, f'{height}', 
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# Labels and Title
        ax.set_xlabel('Day of the Week')  

        ax.set_ylabel('Order Count')
        ax.set_title('Total Orders per Day')
        st.pyplot(fig) 




with col7:
    st.subheader('Monthly Order Trends')
    # Always use the full dataset for the monthly trend graph
    line = data.groupby('month', as_index=False)['order_id'].count()

    # Ensure months are in chronological order
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    line['month'] = pd.Categorical(line['month'], categories=month_order, ordered=True)
    line = line.sort_values(by='month')

    fig, ax = plt.subplots(figsize=(8, 5))

    # Improved line plot with markers and styling
    ax.plot(line['month'], line['order_id'], marker='o', linestyle='-', color='royalblue', 
            markersize=6, linewidth=2.5, markerfacecolor='orange', markeredgewidth=2, markeredgecolor='darkblue')

    # Add title and labels with improved styling
    ax.set_title('Monthly Order Trends', fontsize=14, fontweight='bold', color='darkblue')
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_ylabel('Order Count', fontsize=12, fontweight='bold')

    # Add grid with light transparency
    ax.grid(True, linestyle='--', alpha=0.6)

    # Display values on each point
    for i, txt in enumerate(line['order_id']):
        ax.text(line['month'].iloc[i], line['order_id'].iloc[i] + 5, f'{txt}', 
                ha='center', fontsize=10, fontweight='bold', color='black')

    # Show the plot in Streamlit
    st.pyplot(fig)


category=data.groupby('pizza_category',as_index=False)['total_price'].sum()
col8,col9=st.columns(2)

with col8:

    st.subheader('Sales per pizza Category')
    if select_month=='Overall':
       
       fig,ax=plt.subplots(figsize=(3,4))
       y=['Chicken','Classic','Supreme','Veggie']

       ax.pie(category['total_price'],labels=y,autopct='%0.2f%%',textprops={'color':'purple','fontsize':7})
       ax.legend(loc=10,fontsize=4)
       st.pyplot(fig)
    else:
        data=data[data['month']==select_month]
       
   
       
        fig,ax=plt.subplots(figsize=(3,4))
        y=['Chicken','Classic','Supreme','Veggie']

        ax.pie(category['total_price'],labels=y,autopct='%0.2f%%',textprops={'color':'purple','fontsize':7})
        ax.legend(loc=4,fontsize=4)
        st.pyplot(fig)

data['pizza_size'].replace({'M':'Medium','L':'Large', 'S':'Small', 'XL':'XLarge', 'XXL':'XXLarge'},inplace=True)
size=data.groupby('pizza_size',as_index=False)['total_price'].sum()
with col9:

        st.subheader('Sales per pizza Size')
        if select_month=='Overall':
       
            fig,ax=plt.subplots(figsize=(3,4))
            y=size['total_price'].unique()
            y1=size['pizza_size'].unique()
            
            marks=[f'{label}:{round(markss,1)}' for label,markss in zip(y1,y)]
            ax.pie(size['total_price'],labels=size['pizza_size'].tolist(),radius=1.5,autopct='%0.2f%%',textprops={'color':'black','fontsize':7})
            ax.pie([1],colors='white')
            ax.legend(loc=10,fontsize=6,labels=marks)
            st.pyplot(fig)

        else:
            data=data[data['month']==select_month]
            
            
   
       
            fig,ax=plt.subplots(figsize=(3,4))
            y=size['total_price'].unique()
            y1=size['pizza_size'].unique()
           
            marks=[f'{label}:{round(markss,1)}' for label,markss in zip(y1,y)]
            ax.pie(size['total_price'],labels=size['pizza_size'].tolist(),radius=1.5,autopct='%0.2f%%',textprops={'color':'black','fontsize':7})
            ax.pie([1],colors='white')
            ax.legend(loc=10,fontsize=6,labels=marks)
            st.pyplot(fig)






col10,col11=st.columns(2)
with col10:
    st.subheader('Top 5 pizza sale by Order')
    top_five=data.groupby('pizza_name',as_index=False)['total_price'].count().sort_values(by='total_price',ascending=False).head(5)
    if select_month=='Overall':
        fig,ax=plt.subplots()
        stem=ax.stem(top_five['pizza_name'],top_five['total_price'])
        for x,y in zip(top_five['pizza_name'],top_five['total_price']):
            ax.text(x,y,f'{y}',ha='center',va='bottom',fontsize=10,fontweight='bold')
        plt.xticks(rotation=22)
        st.pyplot(fig)
    else:
        data=data[data['month']==select_month]
        fig,ax=plt.subplots()
        stem=ax.stem(top_five['pizza_name'],top_five['total_price'])
        for x,y in zip(top_five['pizza_name'],top_five['total_price']):
          ax.text(x,y,f'{y}',ha='center',va='bottom',fontsize=10,fontweight='bold')
        plt.xticks(rotation=22)
        st.pyplot(fig)



with col11:
    st.subheader('Top 5 pizza sale by quantity')
    quantity1=data.groupby('pizza_name',as_index=False)['quantity'].sum().sort_values(by='quantity',ascending=False).head(5)
    if select_month=='Overall':
        fig,ax=plt.subplots()
        stem=ax.stem(quantity1['pizza_name'],quantity1['quantity'])
        for x,y in zip(quantity1['pizza_name'],quantity1['quantity']):
          ax.text(x,y,f'{y}',ha='center',va='bottom',fontsize=10,fontweight='bold')
        plt.xticks(rotation=22)
        st.pyplot(fig)
    else:
        data=data[data['month']==select_month]
        quantity1=data.groupby('pizza_name',as_index=False)['quantity'].sum().sort_values(by='quantity',ascending=False).head(5)
        fig,ax=plt.subplots()
        stem=ax.stem(quantity1['pizza_name'],quantity1['quantity'])
        for x,y in zip(quantity1['pizza_name'],quantity1['quantity']):
          ax.text(x,y,f'{y}',ha='center',va='bottom',fontsize=10,fontweight='bold')
        plt.xticks(rotation=22)
        st.pyplot(fig)



