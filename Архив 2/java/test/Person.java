public abstract class Person {
    public String name;
    public int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public void info() {
        String name2 = name;
        int age2 = age;
        System.out.println("name: " + name + " age: " + age2);
    }

    public void Set_name(String name) {
        this.name = name;
    }
}
