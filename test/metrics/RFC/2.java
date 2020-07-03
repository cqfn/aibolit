import java.util.Scanner;
 
public class Calculator {
    public static void main(String[] args) { // +1
        double num1 = getNumber();
        double num2 = getNumber();
        char operation = getOperation();
        double result = calc(num1, num2, operation);
        System.out.println("Результат:" + result); // +1
    }
 
    public static double getNumber() { // +1
        Scanner sc = new Scanner(System.in); // +1
        System.out.println("Введите число:");
        if(sc.hasNextDouble()) { // +1
            return sc.nextDouble(); // +1
        } else {
            System.out.println("Ошибка при вводе. Повторите ввод");
            return getNumber();
        }
    }
 
    public static char getOperation() { // +1
        Scanner sc = new Scanner(System.in);
        System.out.println("Выберите номер операции:\n1 - прибавить\n2 - отнять\n3 - умножить\n4 - разделить");
        int operationNumber = 0;
        if(sc.hasNextInt()) { // +1
            operationNumber = sc.nextInt();
        } else {
            System.out.println("Вы ввели не число! Повторите ввод!");
            return getOperation();
        }
        switch (operationNumber) {
            case 1:
                return '+';
            case 2:
                return '-';
            case 3:
                return '*';
            case 4:
                return '/';
            default:
                System.out.println("Неправильная операция! Повторите ввод!");
                return getOperation();
        }
    }
 
    public static double add(double num1, double num2) { // +1
        return num1+num2;
    }
 
    public static double sub(double num1, double num2) { // +1
        return num1-num2;
    }
 
    public static double mul(double num1, double num2) { // +1
        return num1*num2;
    }
 
    public static double div(double num1, double num2) { // +1
        if(num2 != 0.0) {
            return num1/num2;
        } else {
            System.out.println("На 0 делить нельзя!");
            return Double.NaN;
        }
    }
 
    public static double calc(double num1, double num2, char operation) { // +1
        switch (operation) {
            case '+':
                return add(num1, num2);
            case '-':
                return sub(num1, num2);
            case '*':
                return mul(num1, num2);
            case '/':
                return div(num1, num2);
            default:
                return Double.NaN;
        }
    }
}