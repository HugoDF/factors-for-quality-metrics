Sub Macro1()
    
TotalRows = ActiveSheet.UsedRange.Rows.Count

Dim s1 As String
Dim s2 As String
Dim s3 As String
Dim s4 As String
Dim PassRate(200) As Double

Dim SheetNo As Integer

ChangeLine = 0

Do While ChangeLine < 21

ChangeLine = ChangeLine + 1
i = 1
Do While i < 201
    SheetNo = 10

    Worksheets("Sheet0").Range("$A$1:$D$134711").AutoFilter Field:=1, Criteria1:=20 * (SheetNo - 1) + ChangeLine
    Worksheets("Sheet0").Range("$A$1:$D$134711").AutoFilter Field:=4, Criteria1:=i

    If Range("a1: a134711").SpecialCells(xlCellTypeVisible).Count > 1 Then
        Range("a2: a134711").SpecialCells(xlCellTypeVisible).Select
        For Each r In Selection
            Sum = Sum + 1
        Next

        Worksheets("Sheet0").Range("$A$1:$D$134711").AutoFilter Field:=2, Criteria1:= _
        "passed"
        If Range("a1: a134711").SpecialCells(xlCellTypeVisible).Count > 1 Then
            Range("a2: a134711").SpecialCells(xlCellTypeVisible).Select
            For Each r In Selection
                PassSum = PassSum + 1
            Next
            PassRate(i) = PassSum / Sum

        Else
            PassRate(i) = 0
        End If

    End If
    Select Case ChangeLine
        Case Is = 1
            s1 = "B"
        Case Is = 2
            s1 = "C"
        Case Is = 3
            s1 = "D"
        Case Is = 4
            s1 = "E"
        Case Is = 5
            s1 = "F"
        Case Is = 6
            s1 = "G"
        Case Is = 7
            s1 = "H"
        Case Is = 8
            s1 = "I"
        Case Is = 9
            s1 = "J"
        Case Is = 10
            s1 = "K"
        Case Is = 11
            s1 = "L"
        Case Is = 12
            s1 = "M"
        Case Is = 13
            s1 = "N"
        Case Is = 14
            s1 = "O"
        Case Is = 15
            s1 = "P"
        Case Is = 16
            s1 = "Q"
        Case Is = 17
            s1 = "R"
        Case Is = 18
            s1 = "S"
        Case Is = 19
            s1 = "T"
        Case Is = 20
            s1 = "U"
        
    End Select
    
    s2 = s1 & CStr(i + 1)
    s3 = "Sheet" & CStr(SheetNo)
    Worksheets(s3).Range(s2).Value = PassRate(i)
    Sum = 0
    PassSum = 0
    i = i + 1
    ActiveSheet.ShowAllData
Loop
 
Loop

End Sub
