// one.java

public class StringExample
{
    public static int methodName(int a, int b)
    {
        if (a > b)
        {
            return a;
        }
        else
        {
            return b;
        }
    }

    public static boolean search_string(String searchme)
    {
        if(searchme.contains("Hello"))
        {
            System.out.println("Hello yourself!");
            return true;
        }
        else
        {
            return false;
        }
    }

    public static boolean check_boss(String searchme)
    {
        boolean gamma;
        if(searchme.contains("newb"))
        {
            gamma = false;
        }
        else if ((searchme.contains("boss")) ||
                 (searchme.contains("cto")))
        {

            gamma = true;
        }
        else
        {
            gamma = false;
        }
        return gamma;
    }

    public static void access_check(boolean gamma)
    {
        if(gamma)
        {
            System.out.println("Affirmative.");
        }
        else
        {
            System.out.println("Negative.");
        }
    }


    public static void main(String[] args)
    {
        String s1 = "Computer Science";
        int x = 307;
        String s2 = s1 + " " + x;
        String s3 = s2.substring(10,17);
        String s4 = "is fun";
        String s5 = s2 + s4;

        System.out.println("s1: " + s1);
        System.out.println("s2: " + s2);
        System.out.println("s3: " + s3);
        System.out.println("s4: " + s4);
        System.out.println("s5: " + s5);

        //showing effect of precedence
        x = 3;
        int y = 5;
        String s6 = x + y + "total";
        String s7 = "total " + x + y;
        String s8 = " " + x + y + "total";
        System.out.println("s6: " + s6);
        System.out.println("s7: " + s7);
        System.out.println("s8: " + s8);

        x = methodName(16,93);
        System.out.println("The greater number is: " + x);

        boolean gamma;
        gamma = search_string("Hello There!");
        access_check(gamma);
        gamma = search_string("How are you?");
        access_check(gamma);

        gamma = check_boss("Hi, I am a senior boss.");
        access_check(gamma);
        gamma = check_boss("Hi, I am a executive cto.");
        access_check(gamma);
        gamma = check_boss("Hi, I am a newb low level boss.");
        access_check(gamma);
    }
}
