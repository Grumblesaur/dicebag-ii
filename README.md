# dicebag ii
https://github.com/Grumblesaur/dicebag-ii.git

`dicebag` is a chatbot for Discord whose primary feature is a mathematical
expression engine intended to be used for rolling random numbers and per-
forming calculations that could be pertinent to tabletop games. It also
supports several common scientific calculator functions.

## dicelang

`dicelang` is the name of the language supported by the mathematical ex-
pression engine. It stands for `Dumb Integrated Chatbot Expression Language
And Number Generator`. Available operations are listed below in order of
operator precedence, from tightest-binding to loosest-binding.

### Operators
```
  () : Parentheses will raise their enclosed expression to the highest level
       of precedence.
  
  
  ^  : The repetition operator. Usage: a ^ b, where `a` is a macro, or a
       string, whose contents are a legal expression in dicelang, and `b`
       is any expression which resolves to an integer. The instructions in
       the macro `a` are repeated `b` times, and returned as a list.
  
  
  d  : The die roll operator. Usage: a d b, where `a` and `b` are both
       expressions that resolve to integers. This operation rolls `a` dice
       each with `b` sides and returns them in a list.
  
  
  l  : The keep-lowest operator. Usage: a l b, where `a` is an expression
       that resolves to a list, and `b` is an expression that resolves to
       an integer. This operation keeps the `b` lowest dice from `a`, and
       returns them in a list.
  
  h  : The keep-highest operator. Usage: a h b, where `a` is an expression
       that resolves to a list, and `b` is an expression that resolves to
       and integer. This operation keeps the `b` highest dice from `a`, and
       returns them in a list.
  
  In the case of both the l and h operators, when their `b` argument is
  equal to 1, they return their result as a scalar (integer or real).
  
  
  #  : The sum operator. Usage: #a, where `a` is an expression that resolves
       to a list. This operation sums all the values in the list and returns
       a scalar (integer or real).
  
  @  : The average operator. Usage: @a, where `a` is an expression that
       resolves to a list. This operation returns the average of the values
       in `a` and returns them as a scalar.
  
  ?  : The statistical operator. Usage: ?a, where `a` is an expression that
       resolves to a list. This operation returns a list of `a`'s total,
       average, maximum, and minimum values, in that order.
  
  :  : The even filter operator. Usage: :a, where `a` is an expression that
       resolves to a list. This operation returns a list of all of the even
       numbers in `a`.
  
  &  : The odd filter operator. Usage: &a, where `a` is an expression that
       resolves to a list. This operation returns a list of all of the odd
       numbers in `a`.
  
  
  ** : The exponentiation operator. Usage: a ** b, where `a` and `b` are 
       both expressions that resolve to a scalar (integer or real). This
       operation returns `a` to the power of `b` as a scalar result.
  
  ~  : The logarithm operator. Usage: a ~ b, where `a` and `b` are both
       expressions that resolve to a scalar (integer or real). This
       operation returns log base `a` of `b` as a scalar result.
  
  
  c  : The binomial coefficient operator. Usage a c b, where `a` and `b` are
       both expressions that resolve to an integer and `a` > `b`. This
       operation returns the factorial of `a` divided by (the factorial of
       `b` times the factorial of (`a` minus `b`)) as an integer.
  
  
  !  : The factorial operator. Usage: a!, where `a` is an expression that
       resolves to an integer. This operation returns the factorial of `a`
       as an integer.
  
  
  %% : The root operator. Usage: a %% b, where `a` and `b` are both
       expressions that resolve to a scalar. This operation returns the
       `a`th root of `b` as a scalar.
  
  
  +  : The unary plus operator. Usage: +a, where `a` is an expression that
       resolves to a scalar. This operation returns the absolute value of
       `a` as a scalar.
  
  -  : The unary minus operator. Usage: -a, where `a` is an expression that
       resolves to a scalar. This operation returns `a` with an inverted
       sign as a scalar.
  
  
  *  : The multiplication operator. Usage: a * b, where `a` and `b` are both
       expressions that resolve to a scalar. This operation returns the
       product of `a` times `b` as a scalar.
  
  /  : The division operator. Usage: a / b, where `a` and `b` are both
       expressions that resolve to a scalar. This operation returns the
       quotient of `a` divided by `b` as a scalar.
  
  // : The floored division operator. Usage: a // b, where `a` and `b` are
       both expressions that resolve to scalars. This operation returns the
       quotient of `a` / `b`, always rounded down, as an integer.
  
  %  : The remainder division operator. Usage: a % b, where `a` and `b` are
       both expressions that resolve to integers. This operation returns
       the remainder of `a` // `b` as an integer.
  
  
  +  : The binary plus operator. Usage: a + b, where `a` and `b` are both
       expressions that resolve to any type, as long as both are of the
       same type. For macro strings or lists, this operation returns the
       concatenation of `a` and `b`. For scalars, this operation returns
       the sum of `a` and `b`.
  
  -  : The binary minus operator. Usage: a - b, where `a` and `b` are both
       expressions that resolve to scalars. This operation returns the
       difference between `a` and `b`.
  
  
  
  <  : The less-than operator. Usage: a < b, where `a` and `b` are both
       expressions that resolve to the same type. This operation returns
       1 if `a` is less than `b`, otherwise, 0.
  
  >  : The greater-than operator. Usage: a > b, where `a` and `b` are both
       expressions that resolve to the same type. This operation returns
       1 if `a` is greater than `b`, otherwise, 0.
  
  == : The equality operator. Usage: a == b, where `a` and `b` are both
       expressions. This operation returns 1 if `a` and `b` are the same
       value, otherwise 0.
  
  != : The inequality operator. Usage: a != b, where `a` and `b` are both
       expressions. This operation returns 1 if `a` and `b` are different
       values, otherwise 0.
  
  >= : The greater-equal operator. Usage: a >= b, where `a` and `b` are both
       expressions of the same type. This operation returns 1 if `a` is at
       least as great as `b`, otherwise 0.
  
  <= : The less-equal operator. Usage: a <= b, where `a` and `b` are both
       expressions of the same type. This operation returns 1 if `a` is at
       least as small as `b`, otherwise 0.
  
  
  not: The boolean complement operator. Usage: not a, where `a` is an
       expression of any type. This operation returns 1 when `a` is a
       "falsy" value, like `[]`, `0`, or `''`, and otherwise 0.
  
  and: The boolean conjunction operator. Usage: a and b, where `a` and `b`
       are expressions of any type. This operation returns 0 when either
       `a` or `b` are "falsy" values and `b`  when both are.
  
  or : The boolean disjunction operator. Usage: a or b, where `a` and `b`
       are expressions of any type. This operation returns `a` if `a` is
       not "falsy", `b` if `a` is "falsy" and `b` isn't, or 0 otherwise.
  
  
  $  : The digit concatenation operator. Usage: a $ b, where `a` and `b`
       are expressions that resolve to scalars. This operation coerces both
       `a` and `b` to integers, concatenates the digits of `b` onto the low
       end of `a`, and returns the result as an integer.
  
  
  =  : The assignment operator. Usage: a = b, where `a` is an identifier and
       `b` is any expression. This operation stores `b` in `a`, and returns
       `b`.
  
  
ifelse: The conditional operator. Usage: a if b else c, where `a`, `b`, and
       `c` are all expressions of any type. This operation returns `a` when
       `b` is not "falsy", otherwise it returns `c`.
       
        Alternate usage: a if else b, where `a` and `b` are expressions of
        any type. This operation returns `a` when `a` is not "falsy", 
        otherwise it returns `b`.   
        
        
        Certain operators are vectorized, by wrapping them in angle brackets,
        such as <*>, <$>, <+>, where the left and right operands are each
        each a list. These operations itemwise iterate through the contents
        of the operands and applies the function of the operator to each
        pair of elements, appending result to a list, which is the output.


        It is also possible to treat variables as structures with other
        values contained within. To create an empty structure, use this syntax:
        
          identifier_name = { }
        
        This will initialize the variable  identifier_name  as an empty
        structure. There are two equivalent syntactic forms for editing the
        values contained within the structure.
        
          identifier_name <- field_name , expression
        
        A field can be accessed as a part of an expression, merely by
        using the bracket syntax:
        
          identifier_name['field_name']
        
        This will return the value of  field_name  in  identifier_name.
        
```







