import json
from concurrent.futures import ProcessPoolExecutor
import requests
import logging


def getDataOfPages(pages):
    subs = []
    users = []
    for page in range(1, pages+1):
        print(f'processing page {page}')
        url = f'https://leetcode.com/contest/api/ranking/weekly-contest-257/?pagination={page}'
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


def formatData(data):
    questionSubPair = []

    for key in data:
        question_id = data[key]['question_id']
        submission_id = data[key]['submission_id']
        questionSubPair.append((question_id, submission_id))
    data_region = data[key]['data_region']
    question_id = data[key]['question_id']
    # return (data_region, questionSubPair, data)
    return data


def getQuestionInfo(subId):
    logger.info(f"Getting info for {subId=}")
    url = f'https://leetcode.com/api/submissions/{subId}'
    res = requests.get(url, {})
    data = res.json()
    logger.info(f"Info recieved for {subId=} completed")
    return data['lang'], data['code']


def filterSubmission(submissionInfo):
    contestentData = []
    for idx, data in enumerate(submissionInfo):
        data_region, questionSubPair = formatData(data)
        if data_region != 'CN':
            contestentData.append((data_region, questionSubPair))
        if idx == 1:
            break
    return contestentData


def getCodeLangForSubIds(contestantData):
    global count, total
    print(f'Processing {count} of {total}')
    count[0] += 1
    data_region, questionSubPair = contestantData
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
    return contestModel


def getCodeLangForSubIdsMulti(contestantData):
    global count, total
    count[0] += 1
    print(f'Processing {count} of {total}')
    data_region, questionSubPair = contestantData
    contestModel = {}
    contestModel['data_region'] = data_region
    contestModel['question_ids'] = []
    submission_ids = [submission_id for question_id,
                      submission_id in questionSubPair]
    with ProcessPoolExecutor() as executor:
        output = executor.map(getQuestionInfo, submission_ids)

    langCodes = [x for x in output]
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
    return contestModel


def normalCall(contestantData):
    contestDataWithCode = []
    for contestIndex, contestantData in enumerate(contestantData):
        contestModel = getCodeLangForSubIds(contestantData)
        contestDataWithCode.append(contestModel)
    return contestDataWithCode


def multiCall(contestantData):
    with ProcessPoolExecutor() as executor:
        output = executor.map(getCodeLangForSubIdsMulti, contestantData)
    contestDataWithCode = [x for x in output]
    return contestDataWithCode


count = [0]
total = 0


def main(mode='normal'):

    logger.info('Data load from file started')
    with open('out.json', 'r') as f:
        s = f.read()

    logger.info('Data load complete')

    data = json.loads(s)
    submissionInfo = data
    contestantData = filterSubmission(submissionInfo)

    global total
    total = len(contestantData)
    print(contestantData)
    return None
    logger.info('Data Formatted Successfully')
    if mode == 'normal':
        contestDataWithCode = normalCall(contestantData)
    else:
        contestDataWithCode = multiCall(contestantData)

    print(contestDataWithCode.__len__())

    # contestDataWithCodeJson = json.dumps(contestDataWithCode, indent=4)
    # with open(f'{mode}_finalData.json', 'w') as f:
    # f.write(contestDataWithCodeJson)


if __name__ == "__main__":
    formatter = '%(asctime)s %(pathname)s %(message)s'
    logging.basicConfig(filename="newfile.log",
                        format=formatter,
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    logger.info('Starting process')

    # main()
    # main(mode='multi')
    getDataOfPages(1)

    logger.info('Process Completed')
