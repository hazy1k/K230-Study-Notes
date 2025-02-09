# 第一章 MicroPython基础

1. 注释

```python
# 单行注释
"""
多行注释
"""
print("注释学习")
```

2. 运算符

```python
print(10 + 5) # 加法
print(10 - 5) # 减法
print(10 * 5) # 乘法
print(10 / 5) # 除法
print(7 // 3) # 整除
print(7 % 3)  # 取余
print(3 ** 2) # 指数
```

3. 数据类型转换

```python
x = 3.14
# 将x转换为整数
x1 = int(x)
print(x1)
y = 3
# 将y转换为浮点数
y1 = float(y)
print(y1)
z = 123
z1 = str(z)
print("将整数转换为字符串:", z1)
# 将布尔值转换为字符串
b = True
b1 = str(b)
print("将布尔值转换为字符串:", b1)
```

4. 字符串

```python
# 字符串定义
a = 'Hello K230'     # 单引号定义
b = "Hello K230"     # 双引号定义
c = """Hello K230""" # 三引号定义
d = 'Hello'
# 字符串拼接
print(d + 'K230')
# 字符串格式化
name = "卢本伟"
age = 18
height = 1.80
inf = "我叫%s，已经%d啦，身高%.2f米。" % (name, age, height)
print(inf)

```

5. 判断

```python
# if判断
age = 100
if age >= 18:
    print("你可以干xxx了")
elif age >= 20:
    print("你都超过20岁了，可以干xxx了")
else:
    print("你还没成年哦")
    
```

6. 循环

```python
# while循环
i = 0
while i < 5:
    print("i = %d" % i)
    i += 1
# for循环
name = "K230"
for x in name:
    print(x)
    
```

7. 函数

```python
# 函数定义
def k230(x):
    for i in range(x):
        print(i)
# 函数调用
k230(3)

```

8. 类与继承

```python
# 定义一个类
class k230:
    def __init__(self, a):  # 构造函数
        self.a = 1  # 实例变量

    def method(self):
        pass  # 方法实现


# 实例化对象
obj = k230("hello")
# 访问属性
obj.a = 2  # 修改实例变量
print(obj.a)  # 输出实例变量
# 调用方法
obj.method()


# 继承
class Child(k230):
    def __init__(self, a, child_a):  # 修正构造函数
        super().__init__(a)  # 调用父类构造函数
        self.child_a = child_a  # 添加子类特有的属性


# 实例化子类对象
child_obj = Child("hello", "child_value")
print(child_obj.a)  # 输出父类的实例变量
print(child_obj.child_a)  # 输出子类的实例变量

```
