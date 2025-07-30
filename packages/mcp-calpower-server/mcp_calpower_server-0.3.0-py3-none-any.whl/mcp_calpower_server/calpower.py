# -*- coding: utf-8 -*-
from mcp.server.fastmcp import FastMCP
 
mcp = FastMCP("calpower")

@mcp.tool(name='乘方计算器', description='乘方计算器，输入请求')
async def calculate(expression: str) -> float:
    """Calculates the power need in the given expression
    Args:
        expression (str): The expression to calculate
    Returns:
        result (float): The calculation result
    """

    try:
        # 处理 "8的2.7次方" 格式
        if '的' in expression and '次方' in expression:
            parts = expression.split('的')
            base = float(parts[0])
            power = float(parts[1].replace('次方', ''))
            return base ** power
            
        # 处理 "2.7个8相乘" 格式
        elif '个' in expression and '相乘' in expression:
            parts = expression.split('个')
            power = float(parts[0])
            base = float(parts[1].replace('相乘', ''))
            return base ** power
            
        # 处理 "8**2.7" 或 "8^2.7" 格式
        elif '**' in expression or '^' in expression:
            if '**' in expression:
                base, power = map(float, expression.split('**'))
            else:
                base, power = map(float, expression.split('^'))
            return base ** power
            
        else:
            raise ValueError("不支持的表达式格式")
            
    except Exception as e:
        raise ValueError(f"计算表达式时出错: {str(e)}")

def run():
    mcp.run(transport='stdio')
if __name__ == '__main__':
    run()