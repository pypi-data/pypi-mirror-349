class Header(object):

    TEP_HEADER = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhbm9ueW1vdXNVc2VyIiwiYXV0aCI6InVzZXIiLCJpc3MiOiJzaGVpbiIsImV4cCI6NDEwMjMyOTYwMCwiaWF0IjoxNjUyNzY1NzU5fQ.UtLfIAWLHGtGvgPacPm4Ty_fwQeRmskVpvCwO86kdMU",
        "Content-Type": "application/json"
    }


class Host(object):

    TEP_URL = "https://tep.wrccorp.cn"
    TEP_TEST_URL = "https://tep-test.wrccorp.cn"
    IMG_URL = "http://imgdeal-test01.wrc.com"
    RISK_URL = "http://risk-test-service-cneast-test-test01.test.paas-test.wrccorp.cn"


class Uri(object):

    MEMBER_ID = "/api/testing/aims/locationMember"
    DELETE_PICKUP_ADDRESS = "/api/testing/aims/delTestStoreAddress"
    PAYMENT_REPORT = "/api/testing/report"
    TESTCASE_REPORT = "/api/testing/report/record"
    WHITE_COOKIES = "/api/testing/inventory/api/v1/assets/whitelist_cookies"
    ADD_COOKIES = "/api/testing/inventory/api/v1/assets/tep_cookies"
    MAIL_RECORD = "/api/testing/mmp/msg/queryMailRecord"
    SMS_RECORD = "/api/testing/mmp/msg/querySmsRecord"
    WHATSAPP_RECORD = "/api/testing/mmp/msg/queryWhatsappRecord"
    MAIL_CONTENT = "/api/testing/mmp/msg/queryMailContent"
    TESTCASE_UPLOAD = "/api/testing/testcase/upload"
    TESTCASE_ETP = "/api/testing/testcase/etp"
    IMG_SERVER_UPLOAD = "/index.php/uploadimg"
    MARKETING = "/api/testing/marketLink"
    RISK_SDK_UPLOAD = "/risk-test/risk/sdk/collect"

