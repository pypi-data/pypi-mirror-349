from mcp.server.fastmcp import FastMCP
import pymysql
import logging

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='mysql_mcp.log'
)
logger = logging.getLogger('mysql_mcp')

mcp = FastMCP("MySQLMCP")

@mcp.tool()
def analysis_data(age: int) -> int:
    logger.info(f"Received request to analyze data for age > {age}")
    
    try:
        # 连接数据库
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="Roche123",
            database="mcp",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        logger.info("Successfully connected to the database")
        
        try:
            with conn.cursor() as cursor:
                # 使用参数化查询防止SQL注入
                sql = "SELECT COUNT(*) as count FROM user WHERE age > %s"
                cursor.execute(sql, (age,))
                result = cursor.fetchone()
                count = result['count']
                logger.info(f"Query executed successfully. Result: {count}")
                return count
        finally:
            conn.close()
            logger.info("Database connection closed")
            
    except pymysql.Error as e:
        error_msg = f"Database error: {e}"
        logger.error(error_msg)
        # 可以考虑返回错误信息或默认值
        return 0
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        logger.error(error_msg)
        return 0

if __name__ == "__main__":
    try:
        logger.info("Starting MySQL MCP server...")
        mcp.run()
    except Exception as e:
        logger.exception("Failed to start server")
        raise
