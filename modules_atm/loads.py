import utils

def dla():
    q='''select ACCOUNT_HOLDER as NAME,
        ACCOUNT_NUMBER as ACCOUNT_NO ,SPIN as PIN,"Q1: NAME OF FAVOURITE MOVIE" as a1,
        "Q2: NAME OF BIRTH CITY" as a2,"Q3: FAVOURITE COLOUR" as a3,
        HSPIN as "HIGH-SEQURITY PIN",TWPIN as "TRANSACTION-WITHDRAWL PIN", AMOUNT
        from ACCOUNT
        LIMIT 1
        '''
    data=utils.query_db(q,None,1)
    if not data:
        return None
    return{
        "NAME" : data[0],
        "ACCOUNT_NO" : data[1],
        "PIN" : data[2],
        "a1": data[3],
        "a2": data[4],
        "a3": data[5],
        "HIGH-SEQURITY PIN" : data[6],
        "TRANSACTION-WITHDRAWL PIN" : data[7],
        "AMOUNT" : data[8]
    }