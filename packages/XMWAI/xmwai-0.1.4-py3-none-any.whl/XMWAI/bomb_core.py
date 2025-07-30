import turtle
import time


def bomb(screen, x, y):
    """显示炸弹爆炸动画（包含坐标检查和自动预加载）"""
    # 检查是否为(0,0)坐标
    if x == 0 and y == 0:
        screen.tracer(False)
        warn = turtle.Turtle()
        warn.hideturtle()
        warn.penup()
        warn.goto(0, 0)
        warn.color("#B39F2F")  # 使用指定的金色/橄榄色
        warn.write("不能打击自己", align="center", font=("微软雅黑", 16, "bold"))
        screen.update()
        time.sleep(1.5)
        warn.clear()
        screen.update()
        screen.tracer(True)
        return

    # 预加载所有炸弹GIF形状（首次调用时执行）
    if not hasattr(bomb, "_gif_loaded"):
        for i in range(86):
            screen.addshape(f"/gif/{i}.gif")
        bomb._gif_loaded = True
    
    # 正常爆炸动画流程
    screen.tracer(False)
    b = turtle.Turtle()
    b.penup()
    b.goto(x, y + 70)
    
    for i in range(86):
        b.shape(f"gif/bomb-{i:02d}.gif")
        time.sleep(0.01)
        screen.update()

    b.hideturtle()
    text = f" 💥 成功打击\n坐标({x}, {y})"
    b.pencolor("white")
    b.goto(x, y - 35)
    b.write(text, align="center", font=("微软雅黑", 12))
    
    screen.update()
    time.sleep(1.5)
    b.clear()
    screen.update()
    screen.tracer(True)
