public class Person2 extends Person {
    protected byte height;

    public Person2(String name, int age, byte height) {
        this.name = name;
        this.age = age;
        this.height = height;
    }

    public void info() {
        System.out.println("name: " + this.name + " age: " + this.age + " height: " + this.height);
    }

    @Override // создание метода из родительского класса с другими параметрами
    public void Set_name(String name) {
        super.Set_name(name); // вызов метода из родительского
    }
}