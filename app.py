import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from dash.exceptions import PreventUpdate
import pandas as pd

file_name = 'ProcessedTweets.csv'
tweets_df = pd.read_csv(file_name, lineterminator='\n')
tweets_df.columns = tweets_df.columns.str.replace('\r', '')
tweets_df = tweets_df.rename(columns = {'Dimension 1':'Dimension_1', 'Dimension 2':'Dimension_2'})

# RawTweet, Month, Dimension_1, Dimension_2, Sentiment, Subjectivity
# Test
# print(tweets_df)

'''
Functionalities to Implement:

1. Dropdown Menu for Month Selection:
 o Populate the dropdown with unique months extracted from the dataset. This allows users to filter tweets by month. (10pts)

2. Range Sliders for Sentiment and Subjectivity:
 o Implement range sliders to filter tweets based on their sentiment and subjectivity scores.
 o Make sure to dynamically set the minimum and maximum values of the sliders based on the dataset. (20pts)

3. Scatter Plot:
 o Visualize tweets on a scatter plot based on Dimension 1 and Dimension 2 values.
 o You can use Dimension 1 as the x axis of the scatter plot and Dimension 2 as the y axis. (10pts)

4. Tweet Display Table:
 o Show the texts of selected tweets in a table format.
 o Update the table based on scatter plot selections. (25pts)

5. Callbacks:
 o Implement callbacks to update the scatter plot based on the selected month and the ranges selected for sentiment and subjectivity. (No pts?)

6. Implement another callback to update the tweet display table based on the selected points in the scatter plot and the filters applied. (25pts)

7. Styling and Layout:
 o Organize the components logically and customize the appearance of the scatter plot and table to enhance readability as displayed in the picture above.
 o Notice that the scatter plot does not have a title as well as the axis labels.
 o Also, observe that the modebar is positioned on the right side of the scatter plot and the table data is center aligned. (10pts)

 '''

months = tweets_df.Month.unique()
min_sent = tweets_df.Sentiment.min()
max_sent = tweets_df.Sentiment.max()
min_sub = tweets_df.Subjectivity.min()
max_sub = tweets_df.Subjectivity.max()
'''
# Test
print(months)
print(str(min_sent))
print(str(max_sent))

print(type(min_sent))
print(type(max_sent))

print((str(min_sub)))
print((str(max_sub)))
'''

month_dropdown = dcc.Dropdown(  id = "m_dropdown",
                                options = months,
                                value = months[0],
                                placeholder = 'Select a month',
                                style = dict(width = 150))

# For the sliders, dynamically set the min and max
sentiment_slider = dcc.RangeSlider( min = -1.0,
                                    max = 1.0,
                                    step = 0.1,
                                    id = "sen_slider",
                                    value = [-1.0, 1],
                                    marks = {-1.0: '-1.0', 1.0: '1.0'},
                                    allowCross = False,
                                    tooltip = {"placement": "bottom", "always_visible": True})
subjectivity_slider = dcc.RangeSlider(  min = 0.0,
                                        max = 1.0,
                                        step = 0.1,
                                        id = "sub_slider",
                                        value = [0.0, 1],
                                        marks = {0.0: '0.0', 1.0: '1.0'},
                                        allowCross = False,
                                        tooltip = {"placement": "bottom", "always_visible": True})

# X-Axis = Dimension 1
# Y-Axis = Dimension 2
fig = px.scatter(   tweets_df,
                    x = 'Dimension_1',
                    y = 'Dimension_2')
fig.update_layout(  dragmode = 'lasso')
fig.show()

app = dash.Dash(__name__)
server = app.server

'''
Row 1 = m_dropdown + sen_slider + sub_slider
Row 2 = fig
Row 3 (Eventually) = A table

Row 1 = 15% Total --> 13% Height + 2% Bottom Margin
Row 2 = 45% Total --> 43% Height + 2% Bottom Margin
Row 3 = 35% Total --> 30% Height + 5% Bottom Margin
95% Height Used

'''

# Test
# print ("layout started")

'''








Important Comment:

I don't know what's going wrong with my sliders
It doesn't show the range






'''

app.layout = html.Div(id = 'parent_div', children = [
    html.Div(id = 'row_1', children = [
        month_dropdown,
        sentiment_slider,
        subjectivity_slider
    ]),
    html.Div(id = 'row_2', children = [
        dcc.Graph(id = 'graph_1', figure = fig, style = dict(width = '100%'))
    ]),
    html.Div(id = 'row_3', children = [
        # Empty for now
    ])
])

# Test
# print ("layout finished")

# START OF CALLBACK CODE



# m_dropdown
# sen_slider
# sub_slider
@app.callback(Output('graph_1', 'figure'),
              Input('m_dropdown', 'value'),
              Input('sen_slider', 'value'),
              Input('sub_slider', 'value'),
              prevent_initial_call = True)
def update_graph(drop_val, range_sen, range_sub):
    # Test
    # print('update_graph called')
    found_one = False
    if(drop_val is not None):
        # Test
        # print('dropdown called')
        # The figure should show data only from entries with (month == correct)
        found_one = True
        filtered_tweets1 = tweets_df.loc[tweets_df.Month == drop_val]
    if(range_sen is not None):
        # Test
        print('range sentiment called')
        print(range_sen)
        # From a given month, the figure should show data only from entries with (min <= sentiment <= max) == correct
        found_one = True
        filtered_tweets2 = tweets_df.loc[tweets_df.Sentiment >= range_sen[0]]
        filtered_tweets2 = filtered_tweets2.loc[filtered_tweets2.Sentiment <= range_sen[1]]
    if(range_sub is not None):
        # Test
        print('range subjectivity called')
        print(range_sub)
        # Furthermore, the figure should show data only from entries with (min <= subjectivity <= max) == correct
        found_one = True
        filtered_tweets3 = tweets_df.loc[tweets_df.Subjectivity >= range_sub[0]]
        filtered_tweets3 = filtered_tweets3.loc[filtered_tweets3.Subjectivity <= range_sub[1]]
    if(found_one == True):
        # Now, we can graph the scatterplot with the filtered datapoints
        filtered_tweets = filtered_tweets1.merge(filtered_tweets2).merge(filtered_tweets3)
        fig = px.scatter(   filtered_tweets,
                            x = 'Dimension_1',
                            y = 'Dimension_2')
        # Test
        print('returned fig')
        return fig
    else:
        raise PreventUpdate



# END OF CALLBACK CODE

# Test
# print ("end of code")

if __name__ == '__main__':
    app.run_server(debug=True,port=5001)
