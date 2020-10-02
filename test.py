    #
    #
    # # open log file
    # try:
    #     pages = ['NextSong']
    #     with open('2018-11-20-events.json') as fp:
    #         count = 0
    #         for line in fp:
    #             # print(line)
    #             # pd.read_json()
    #             df = pd.DataFrame(json.loads(line), index=[0])
    #             # print(df[0]['page'])
    #             # df = df['NextSong'].eq('NextSong')
    #             # df.loc[df['Customer'].isin(kids)]
    #             df = df.loc[df['page'] == 'NextSong']
    #             if not df.empty:
    #                 time_data = None
    #                 column_labels = None
    #                 time_df = ()
    # except Exception as e:
    #     print(e)