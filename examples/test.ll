; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"snprintf"(i8* %".1", i64 %".2", i8* %".3", ...)

declare i32 @"puts"(i8* %".1")

declare void @"exit"(i32 %".1")

define i32 @"main"()
{
.2:
  br i1 true, label %"if_then", label %"elif_test_0"
if_merge:
  ret i32 0
if_then:
  ret i32 2
elif_test_0:
  br i1 false, label %"elif_then_0", label %"if_else"
elif_then_0:
  ret i32 3
if_else:
  ret i32 1
}
