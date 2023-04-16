Attribute VB_Name = "画像均等配置"



Sub InsertPicturesAndFilenames()
  Dim strFile As Variant
  Dim objPicture As Object
  Dim i As Integer

  ' 選択した画像のファイル名を全て取得する
  strFile = Application.GetOpenFilename(FileFilter:="PNG Files (*.png),*.png", MultiSelect:=True)

  If TypeName(strFile) = "Boolean" Then
    MsgBox "画像が選択されていません。"
    Exit Sub
  End If

' 選択した画像の数だけ処理を繰り返す
  For i = LBound(strFile) To UBound(strFile)
    ' 画像を挿入する
    Set objPicture = ActiveSheet.Pictures.Insert(strFile(i))

    ' 画像の上にファイル名を表示する
    ActiveSheet.Shapes.AddLabel(msoTextOrientationHorizontal, objPicture.Left, objPicture.Top, objPicture.Width, objPicture.Height).TextFrame.Characters.Text = Mid(strFile(i), InStrRev(strFile(i), "\") + 1)
    With objPicture
      .Top = .Top
      .Left = .Left
      .Width = 190
      .Height = 190
    End With
    
  Next i

End Sub

Sub seiretu()
Dim i As Long

Application.ScreenUpdating = False
With ActiveSheet
  If .Shapes.Count >= 2 Then
    .Shapes(2).Top = .Shapes(1).Top + .Shapes(1).Height + 30
    For i = 3 To .Shapes.Count
      .Shapes(i).Top = .Shapes(i - 1).Top + .Shapes(i - 1).Height + 30
    Next
  End If
End With
Application.ScreenUpdating = True

End Sub


Sub group()
Dim objCount As Long
objCount = ActiveSheet.Shapes.Count

MsgBox = objCount
'For i = 2 To [objCount] Step 2
    '[object i].Top = [object i - 1].Top + [object i - 1].Height
'Next i

End Sub
