import json
from concurrent.futures import ProcessPoolExecutor
import requests
import logging
from time import sleep
contest_id=222

def getDataOfPages(pages):
    subs = []
    users = []
    for page in range(1, pages+1):
        print(f'processing page {page}')
        url = f'https://leetcode.com/contest/api/ranking/weekly-contest-257/?pagination={page}'
        url = f'https://leetcode.com/contest/api/ranking/weekly-contest-{contest_id}/?pagination={page}'
        res = requests.get(url, {})
        data = res.json()
        subs.extend(data['submissions'])
        users.extend(data['total_rank'])

    subs = tuple(subs)
    users = tuple(users)
    data = [subs, users]
    obj = []
    for sub, user in zip(subs, users):
        data = {'subs': sub, 'users': user}
        obj.append(data)
    with open('out.json', 'w') as f:
        f.write(json.dumps(obj, indent=4))


def formatData(allInfo):
    questionSubPair = []
    data = allInfo['subs']
    for key in data:
        question_id = data[key]['question_id']
        submission_id = data[key]['submission_id']
        questionSubPair.append((question_id, submission_id))
    data_region = data[key]['data_region']
    question_id = data[key]['question_id']
    return (data_region, questionSubPair, allInfo['users'])


def getQuestionInfo(subId):
    url = ''
    url += f'https://leetcode.com/api/submissions/{subId}'
    res = requests.get(url, {})
    if res.status_code == 200:
        data = res.json()
        print(f'{res.status_code=}')
        return data['lang'], data['code']
    print(f'{res.status_code=}')
    raise Exception
    return ('', '')


def filterSubmission(submissionInfo):
    contestentData = []
    for idx, data in enumerate(submissionInfo):
        data_region, questionSubPair, other = formatData(data)
        if data_region != 'CN':
            contestentData.append((data_region, questionSubPair, other))
        # if idx == 18:
            # break
    return contestentData


def getCodeLangForSubIds(contestantData):
    global count, total
    print(f'Processing {count} of {total}')
    count[0] += 1
    data_region, questionSubPair, other = contestantData
    contestModel = {}
    contestModel['data_region'] = data_region
    contestModel['question_ids'] = []
    for question_id, submission_id in questionSubPair:
        lang, code = getQuestionInfo(submission_id)
        question = {
            'question_id': question_id,
            'submission_id': submission_id,
            'lang': lang,
            'code': code,
        }
        contestModel['question_ids'].append(question)
    contestModel['username'] = other['username']
    contestModel['rank'] = other['rank']
    return contestModel


def getCodeLangForSubIdsMulti(contestantData):
    global count, total
    count[0] += 1
    print(f'Processing {count} of {total}')
    data_region, questionSubPair, other = contestantData
    contestModel = {}
    contestModel['data_region'] = data_region
    contestModel['question_ids'] = []
    submission_ids = [submission_id for question_id,
                      submission_id in questionSubPair]
    with ProcessPoolExecutor() as executor:
        # loutput = executor.map(getQuestionInfo, submission_ids)

        futures = [executor.submit(getQuestionInfo, sid)
                   for sid in submission_ids]
    langCodes = [f.result() for f in futures]
    for idx, langCode in enumerate(langCodes):
        lang, code = langCode
        question_id, submission_id = questionSubPair[idx]
        question = {
            'question_id': question_id,
            'submission_id': submission_id,
            'lang': lang,
            'code': code,
        }
        contestModel['question_ids'].append(question)
    contestModel['username'] = other['username']
    contestModel['rank'] = other['rank']
    return contestModel


def normalCall(contestantData):
    contestDataWithCode = []
    for contestIndex, contestantData in enumerate(contestantData):
        contestModel = getCodeLangForSubIdsMulti(contestantData)
        contestDataWithCode.append(contestModel)
    return contestDataWithCode


def multiCall(contestantData):
    lenOfData = len(contestantData)
    contestDataWithCode = []
    size = 5
    try:
        for low in range(0, lenOfData, size):
            with ProcessPoolExecutor(size) as executor:
                futures = [executor.submit(getCodeLangForSubIdsMulti, data)
                           for data in contestantData[low:low+size]]
            contestDataWithCode.extend([f.result() for f in futures])
            sleep(10)
    except Exception as e:
        print(e)
    finally:
        return contestDataWithCode


count = [0]
total = 0
isNew = False


def writeToFile(data):
    dataJson = json.dumps(data, indent=4)
    with open(f'finalData_{contest_id}.json', 'w') as f:
        f.write(dataJson)


def main(mode='normal'):

    with open('out.json', 'r') as f:
        s = f.read()


    data = json.loads(s)
    submissionInfo = data
    contestantData = filterSubmission(submissionInfo)

    global total
    total = len(contestantData)
    print(contestantData)
    # return None
    if mode == 'normal':
        contestDataWithCode = normalCall(contestantData)
    else:
        contestDataWithCode = multiCall(contestantData)

    print(contestDataWithCode.__len__())
    writeToFile(contestDataWithCode)


if __name__ == "__main__":

    getDataOfPages(3)
    # main()
    main(mode='multi')
    pass

