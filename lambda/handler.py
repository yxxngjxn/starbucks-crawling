import json
from merge import merge_beverage_data

def handler(event, context):
    try:
        data = merge_beverage_data()
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json; charset=utf-8",
                "Access-Control-Allow-Origin": "*",  # 필요 시 CORS 조정
            },
            "body": json.dumps(data, ensure_ascii=False),
        }
    except Exception as e:
        # CloudWatch 로그로 확인할 수 있도록
        print(f"[ERROR] {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}, ensure_ascii=False),
        }