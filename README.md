# pmat

***

## Лабораторная работа №1

1. Переходим в lab1.

```shell
cd lab1
```

2. Делаем файлы random_number.py, divide.py, sqrt.py исполняемыми.

```shell
chmod +x random_number.py
chmod +x divide.py
chmod +x sqrt.py
```

3. Запускаем.

```shell
./random_number.py | ./divide.py 2>> errors.txt | ./sqrt.py 2>> errors.txt
```

***

## Лабораторная работа №2

1. Переходим в lab2.

```shell
cd lab2
```

2. Делаем файл greeting_adapt.py исполняемым.

```shell
chmod +x greeting_adapt.py
```

**Пример 1:**

Содержимое файла names.txt:

```text
maria
Nick
Anna
Ivan
```

```shell
./greeting_adapt.py < names.txt 2> error.txt
```

```text
Nice to see you Nick!
Nice to see you Anna!
Nice to see you Ivan!
```

Содержимое файла error.txt:

```text
Error: Name 'maria' needs to start uppercase!
```

**Пример 2:**

```shell
./greeting_adapt.py
```

```text
Hey, what's your name?
Kirill
Nice to see you Kirill!
Hey, what's your name?
Nicolas
Nice to see you Nicolas!
Hey, what's your name?
aleksandr
Error: Name 'aleksandr' needs to start uppercase!
Hey, what's your name?
A1eksandr
Error: Name 'A1eksandr' contains an invalid character!
Hey, what's your name?
^C
Goodbye!
```
