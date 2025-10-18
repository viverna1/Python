import java.util.Scanner; // для ввода-вывода данных
import java.util.ArrayList; // для работы с массивами

public class Main {
    public static void main(String[] args) {
        System.out.println("hello");

        // типы данных java
        int num; // можно создать переменную без присвоения ей значения
        float num1, num2; // создать несколько переменных одного типа

        int a = 1; // byte до 127, short до 32767, int до 2147483647, long до бесконечности
        float b = 1.0f; // float до 3.4028235E38, double до бесконечности
        boolean c = true;
        char d = 'a';
        String e = "hello";

        // получение данных от пользователя
        Scanner scan = new Scanner(System.in);
        // String name = scan.nextLine();
        // scan.nextLine - получение строки
        // scan.nextInt - получение целого числа
        // scan.nextFloat - получение числа с плавающей точкой
        // и т д

        // массивы
        int[] arr = new int[10]; // ограниченное количество элементов (10)
        arr[0] = 1;
        arr[1] = 2;
        arr[2] = 3;

        ArrayList<Byte> arr1 = new ArrayList<>(); // тип данных писать с большой буквы
        arr1.add((byte) 1); // добавление элемента в конец массива
        arr1.add(1, (byte) 2); // добавление элемента по индексу (он в начале)
        System.out.println(arr1);
        // add - добавление элемента в конец массива
        // get - получение элемента по индексу
        // remove - удаление элемента по индексу
        // size - получение размера массива
        // clear - очистка массива
        // contains - проверка наличия элемента в массиве
        // indexOf - получение индекса элемента в массиве
        // lastIndexOf - получение индекса элемента в массиве с конца
        // set - изменение элемента по индексу
        // sort - сортировка массива
        // reverse - переворот массива
        // subList - получение подмассива по индексам
        // toArray - получение массива из коллекции

        // условные операторы
        if (a == 1) {
            System.out.println("a == 1");
        } else if (a == 2) {
            System.out.println("a == 2");
        } else {
            System.out.println("a!= 1 and a!= 2");
        }

        // switch
        a = 1;
        switch (a) {
            case 1:
                System.out.println("a == 1"); break;
            case 2:
                System.out.println("a == 2"); break;
            default:
                System.out.println("a!= 1 and a!= 2"); break;
        }

        // циклы
        for (int i = 0; i < 10; i++) {
            System.out.println(i);
        }

        for (Byte i : arr1) { // перебор массива
            System.out.println(i);
        }

        while (a < 10) {
            System.out.println(a);
            a++;
        }

        do {
            System.out.println(a);
            a++;
        } while (a < 10);

        // функции
        int sum = summa((byte) 1, (byte) 2);
        print("hello " + sum);

        // классы и объекты
        Person2 person = new Person2("Виви", 16, (byte) 165);
        person.info();
    }

    public static void print(String str) {
        System.out.println(String.valueOf(str));
    }

    public static int summa(byte a, byte b) {
        int res = a + b;
        return res;
    }
}
