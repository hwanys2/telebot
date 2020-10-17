import os
import sys
import urllib.request
import json
from pprint import pprint
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
client_id = "LI0refndXUiudnjF36bN"
client_secret = "7CBFF93cq0"

encText = urllib.parse.quote(""""Introduction
In PISA 2018, mathematics is assessed as a minor domain, providing an opportunity to make comparisons of student performance over time. This framework continues the description and illustration of the PISA mathematics assessment as set out in the 2012 framework, when mathematics was re-examined and updated for use as the major domain in that cycle.
For PISA 2018, as in PISA 2015, the computer is the primary mode of delivery for all domains, including mathematical literacy. However, paper-based assessment instruments are provided for countries that choose not to test their students by computer. The mathematical literacy component for both the computer-based and paper-based instruments are composed of the same clusters of mathematics trend items. The number of trend items in the minor domains (of which mathematics is one in 2018) are increased, when compared to PISA assessments prior to 2015, therefore increasing the construct coverage while reducing the number of students responding to each question. This design is intended to reduce potential bias while stabilising and improving the measurement of trends.
The PISA 2018 mathematics framework is organised into several major sections. The first section, “Defining Mathematical Literacy,” explains the theoretical underpinnings of the PISA mathematics assessment, including the formal definition of the mathematical literacy construct. The second section, “Organising the Domain of Mathematics,” describes three aspects: a) the mathematical processes and the fundamental mathematical capabilities (in previous frameworks the “competencies”) underlying those processes; b)the way mathematical content knowledge is organised, and the content knowledge that is relevant to an assessment of 15-year-old students; and c) the contexts in which students face mathematical challenges. The third section, “Assessing Mathematical Literacy”, outlines the approach taken to apply the elements of the framework previously described, including the structure of the assessment, the transfer to a computer-based assessment and reporting proficiency. The 2012 framework was written under the guidance of the 2012 Mathematics Expert Group (MEG), a body appointed by the main PISA contractors with the approval of the PISA Governing Board (PGB). The ten MEG members included mathematicians, mathematics educators, and experts in assessment, technology, and education research from a range of countries. In addition, to secure more extensive input and review, a draft of the PISA2012 mathematics framework was circulated for feedback to over 170 mathematics experts from over 40 countries. Achieve and the Australian Council for Educational Research (ACER), the two organisations contracted by the Organisation for Economic Co-operation and Development (OECD) to manage framework development, also conducted various research efforts to inform and support development work. Framework development and the PISA programme generally have been supported and informed by the ongoing work of participating countries, as in the research described in OECD (2010[1]). The PISA 2015 framework was updated under the guidance of the mathematics expert group (MEG), a body appointed by the Core 1 contractor with the approval of the PISA Governing Board (PGB). There are no substantial changes to the mathematics framework between PISA 2015 and PISA 2018.
In PISA 2012, mathematics (the major domain) was delivered as a paper-based assessment, while the computer-based assessment of mathematics (CBAM) was an optional domain that was not taken by all countries. As a result, CBAM was not part of the mathematical literacy trend. Therefore, CBAM items developed for PISA 2012 are not included in the 2015 and 2018 assessments where mathematical literacy is a minor domain, despite the change in delivery mode to computer-based.
 PISA 2018 ASSESSMENT AND ANALYTICAL FRAMEWORK © OECD 2019
CHAPTER 3. PISA 2018 MATHEMATICS FRAMEWORK │ 75
 The framework was updated for PISA 2015 to reflect the change in delivery mode, and includes a discussion of the considerations of transposing paper items to a screen and examples of what the results look like. The definition and constructs of mathematical literacy however, remain unchanged and consistent with those used in 2012."""")
data = "source=en&target=ko&text=" + encText  #ko 한국어 타겟 En 영어 
url = "https://openapi.naver.com/v1/papago/n2mt"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request, data=data.encode("utf-8"))
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    # print(response_body.decode('utf-8'))
    res = json.loads(response_body.decode('utf-8'))
    pprint(res['message']['result']['translatedText'])
else:
    print("Error Code:" + rescode)