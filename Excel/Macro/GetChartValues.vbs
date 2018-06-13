Sub GetChartValues()
   Dim NumberOfRows As Integer
   Dim X As Object
   Counter = 2

   ' Calculate the number of rows of data.
   NumberOfRows = UBound(ActiveChart.SeriesCollection(1).Values)

   Worksheets("ChartData").Cells(1, 1) = "X Values"

   ' Write x-axis values to worksheet.
   With Worksheets("ChartData")
      .Range(.Cells(2, 1), _
      .Cells(NumberOfRows + 1, 1)) = _
      Application.Transpose(ActiveChart.SeriesCollection(1).XValues)
   End With

   ' Loop through all series in the chart and write their values to
   ' the worksheet.
   For Each X In ActiveChart.SeriesCollection
      Worksheets("ChartData").Cells(1, Counter) = X.Name

      With Worksheets("ChartData")
         .Range(.Cells(2, Counter), _
         .Cells(NumberOfRows + 1, Counter)) = _
         Application.Transpose(X.Values)
      End With

      Counter = Counter + 1
   Next

End Sub
