Attribute VB_Name = "�摜�ϓ��z�u"



Sub InsertPicturesAndFilenames()
  Dim strFile As Variant
  Dim objPicture As Object
  Dim i As Integer

  ' �I�������摜�̃t�@�C������S�Ď擾����
  strFile = Application.GetOpenFilename(FileFilter:="PNG Files (*.png),*.png", MultiSelect:=True)

  If TypeName(strFile) = "Boolean" Then
    MsgBox "�摜���I������Ă��܂���B"
    Exit Sub
  End If

' �I�������摜�̐������������J��Ԃ�
  For i = LBound(strFile) To UBound(strFile)
    ' �摜��}������
    Set objPicture = ActiveSheet.Pictures.Insert(strFile(i))

    ' �摜�̏�Ƀt�@�C������\������
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
