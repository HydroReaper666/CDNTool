
'''

 File order:
 - 1) Imports (order below)
 - 2) Variable definitions, both XAML objects and global vars
 - 3) Functions and classes (CIA generator, UI class, Web downloader with progress...)
 - 4) Entrypoint, using elements above

 Import order:
 - 1) Python common modules
 - 2) Opuka project's module (info at README.md), providing tools to manage WPF with Python (way more complex than in C# or VB)
 - 3) (After loading .NET Framework support) .NET Framework libraries as modules (thanks to Python.NET, AKA clr module)

 To Do:
 - Check if required tools are there (MahApps and Material DLLs, ctrtool, make_cdn_cia...), otherwise close program

'''

from __future__ import print_function
from clr import AddReference
from urllib import urlretrieve
from win32gui import ShowWindow
from win32console import GetConsoleWindow
from urllib2 import urlopen, HTTPError
from sys import exit, argv, stdout
from os import system, mkdir, listdir, unlink, walk, unlink
from os.path import dirname, realpath, exists, join, isfile, basename
from shutil import rmtree, copyfile
from json import loads
from threading import Thread as PyThread
from pyperclip import copy
from subprocess import Popen, PIPE

from Opuka import XamlObject, Xaml_Dicts, Xaml_Width, Xaml_Height, XamlTitleTemplate, BrushColor, ErrorMessage

AddReference(r"wpf\PresentationFramework")
AddReference("MaterialDesignThemes.Wpf")
AddReference("MaterialDesignColors")
AddReference("MahApps.Metro")

from System import Uri, UriKind, Type, Console
from System.IO import MemoryStream, File
from System.Threading import Thread, ApartmentState, ThreadStart
from System.Reflection import Assembly
from System.Xml import XmlReader
from System.Windows import Window, DataFormats, WindowStyle, DataTemplate, FrameworkElementFactory, ResizeMode, TextWrapping, ResourceDictionary, VerticalAlignment, HorizontalAlignment, Thickness
from System.Windows.Controls import Button, Grid, DataGrid, DataGridTextColumn, StackPanel, RichTextBox, TextBlock, Image, Dock
from System.Windows.Media import Brushes, BrushConverter
from System.Windows.Media.Imaging import BitmapImage
from System.Windows.Markup import XamlReader
from System.Windows.Forms import SaveFileDialog, MessageBoxButtons, MessageBox, DialogResult
from System.Windows.Data import Binding
from System.Threading import Thread, ApartmentState, ThreadStart
from MahApps.Metro.Controls import MetroWindow, WindowCommands

metacetk = [
	0x00, 0x01, 0x00, 0x04, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0,
	0xD1, 0x5E, 0xA5, 0xE0, 0xD1, 0x5E, 0xA5, 0xE0, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x52, 0x6F, 0x6F, 0x74,
	0x2D, 0x43, 0x41, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x33, 0x2D,
	0x58, 0x53, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x63, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0xFE, 0xED, 0xFA, 0xCE, 0xFE, 0xED, 0xFA, 0xCE, 0xFE, 0xED, 0xFA, 0xCE,
	0xFE, 0xED, 0xFA, 0xCE, 0xFE, 0xED, 0xFA, 0xCE, 0xFE, 0xED, 0xFA, 0xCE,
	0xFE, 0xED, 0xFA, 0xCE, 0xFE, 0xED, 0xFA, 0xCE, 0xFE, 0xED, 0xFA, 0xCE,
	0xFE, 0xED, 0xFA, 0xCE, 0xFE, 0xED, 0xFA, 0xCE, 0xFE, 0xED, 0xFA, 0xCE,
	0xFE, 0xED, 0xFA, 0xCE, 0xFE, 0xED, 0xFA, 0xCE, 0xFE, 0xED, 0xFA, 0xCE,
	0x01, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC,
	0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xAA, 0xAA, 0xAA, 0xAA,
	0xAA, 0xAA, 0xAA, 0xAA, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x14, 0x00, 0x00, 0x00, 0xAC,
	0x00, 0x00, 0x00, 0x14, 0x00, 0x01, 0x00, 0x14, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x28, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x84,
	0x00, 0x00, 0x00, 0x84, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x04,
	0x91, 0x9E, 0xBE, 0x46, 0x4A, 0xD0, 0xF5, 0x52, 0xCD, 0x1B, 0x72, 0xE7,
	0x88, 0x49, 0x10, 0xCF, 0x55, 0xA9, 0xF0, 0x2E, 0x50, 0x78, 0x96, 0x41,
	0xD8, 0x96, 0x68, 0x3D, 0xC0, 0x05, 0xBD, 0x0A, 0xEA, 0x87, 0x07, 0x9D,
	0x8A, 0xC2, 0x84, 0xC6, 0x75, 0x06, 0x5F, 0x74, 0xC8, 0xBF, 0x37, 0xC8,
	0x80, 0x44, 0x40, 0x95, 0x02, 0xA0, 0x22, 0x98, 0x0B, 0xB8, 0xAD, 0x48,
	0x38, 0x3F, 0x6D, 0x28, 0xA7, 0x9D, 0xE3, 0x96, 0x26, 0xCC, 0xB2, 0xB2,
	0x2A, 0x0F, 0x19, 0xE4, 0x10, 0x32, 0xF0, 0x94, 0xB3, 0x9F, 0xF0, 0x13,
	0x31, 0x46, 0xDE, 0xC8, 0xF6, 0xC1, 0xA9, 0xD5, 0x5C, 0xD2, 0x8D, 0x9E,
	0x1C, 0x47, 0xB3, 0xD1, 0x1F, 0x4F, 0x54, 0x26, 0xC2, 0xC7, 0x80, 0x13,
	0x5A, 0x27, 0x75, 0xD3, 0xCA, 0x67, 0x9B, 0xC7, 0xE8, 0x34, 0xF0, 0xE0,
	0xFB, 0x58, 0xE6, 0x88, 0x60, 0xA7, 0x13, 0x30, 0xFC, 0x95, 0x79, 0x17,
	0x93, 0xC8, 0xFB, 0xA9, 0x35, 0xA7, 0xA6, 0x90, 0x8F, 0x22, 0x9D, 0xEE,
	0x2A, 0x0C, 0xA6, 0xB9, 0xB2, 0x3B, 0x12, 0xD4, 0x95, 0xA6, 0xFE, 0x19,
	0xD0, 0xD7, 0x26, 0x48, 0x21, 0x68, 0x78, 0x60, 0x5A, 0x66, 0x53, 0x8D,
	0xBF, 0x37, 0x68, 0x99, 0x90, 0x5D, 0x34, 0x45, 0xFC, 0x5C, 0x72, 0x7A,
	0x0E, 0x13, 0xE0, 0xE2, 0xC8, 0x97, 0x1C, 0x9C, 0xFA, 0x6C, 0x60, 0x67,
	0x88, 0x75, 0x73, 0x2A, 0x4E, 0x75, 0x52, 0x3D, 0x2F, 0x56, 0x2F, 0x12,
	0xAA, 0xBD, 0x15, 0x73, 0xBF, 0x06, 0xC9, 0x40, 0x54, 0xAE, 0xFA, 0x81,
	0xA7, 0x14, 0x17, 0xAF, 0x9A, 0x4A, 0x06, 0x6D, 0x0F, 0xFC, 0x5A, 0xD6,
	0x4B, 0xAB, 0x28, 0xB1, 0xFF, 0x60, 0x66, 0x1F, 0x44, 0x37, 0xD4, 0x9E,
	0x1E, 0x0D, 0x94, 0x12, 0xEB, 0x4B, 0xCA, 0xCF, 0x4C, 0xFD, 0x6A, 0x34,
	0x08, 0x84, 0x79, 0x82, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x52, 0x6F, 0x6F, 0x74, 0x2D, 0x43, 0x41, 0x30,
	0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x33, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01,
	0x58, 0x53, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x63, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x13, 0x7A, 0x08, 0x94, 0xAD, 0x50, 0x5B, 0xB6,
	0xC6, 0x7E, 0x2E, 0x5B, 0xDD, 0x6A, 0x3B, 0xEC, 0x43, 0xD9, 0x10, 0xC7,
	0x72, 0xE9, 0xCC, 0x29, 0x0D, 0xA5, 0x85, 0x88, 0xB7, 0x7D, 0xCC, 0x11,
	0x68, 0x0B, 0xB3, 0xE2, 0x9F, 0x4E, 0xAB, 0xBB, 0x26, 0xE9, 0x8C, 0x26,
	0x01, 0x98, 0x5C, 0x04, 0x1B, 0xB1, 0x43, 0x78, 0xE6, 0x89, 0x18, 0x1A,
	0xAD, 0x77, 0x05, 0x68, 0xE9, 0x28, 0xA2, 0xB9, 0x81, 0x67, 0xEE, 0x3E,
	0x10, 0xD0, 0x72, 0xBE, 0xEF, 0x1F, 0xA2, 0x2F, 0xA2, 0xAA, 0x3E, 0x13,
	0xF1, 0x1E, 0x18, 0x36, 0xA9, 0x2A, 0x42, 0x81, 0xEF, 0x70, 0xAA, 0xF4,
	0xE4, 0x62, 0x99, 0x82, 0x21, 0xC6, 0xFB, 0xB9, 0xBD, 0xD0, 0x17, 0xE6,
	0xAC, 0x59, 0x04, 0x94, 0xE9, 0xCE, 0xA9, 0x85, 0x9C, 0xEB, 0x2D, 0x2A,
	0x4C, 0x17, 0x66, 0xF2, 0xC3, 0x39, 0x12, 0xC5, 0x8F, 0x14, 0xA8, 0x03,
	0xE3, 0x6F, 0xCC, 0xDC, 0xCC, 0xDC, 0x13, 0xFD, 0x7A, 0xE7, 0x7C, 0x7A,
	0x78, 0xD9, 0x97, 0xE6, 0xAC, 0xC3, 0x55, 0x57, 0xE0, 0xD3, 0xE9, 0xEB,
	0x64, 0xB4, 0x3C, 0x92, 0xF4, 0xC5, 0x0D, 0x67, 0xA6, 0x02, 0xDE, 0xB3,
	0x91, 0xB0, 0x66, 0x61, 0xCD, 0x32, 0x88, 0x0B, 0xD6, 0x49, 0x12, 0xAF,
	0x1C, 0xBC, 0xB7, 0x16, 0x2A, 0x06, 0xF0, 0x25, 0x65, 0xD3, 0xB0, 0xEC,
	0xE4, 0xFC, 0xEC, 0xDD, 0xAE, 0x8A, 0x49, 0x34, 0xDB, 0x8E, 0xE6, 0x7F,
	0x30, 0x17, 0x98, 0x62, 0x21, 0x15, 0x5D, 0x13, 0x1C, 0x6C, 0x3F, 0x09,
	0xAB, 0x19, 0x45, 0xC2, 0x06, 0xAC, 0x70, 0xC9, 0x42, 0xB3, 0x6F, 0x49,
	0xA1, 0x18, 0x3B, 0xCD, 0x78, 0xB6, 0xE4, 0xB4, 0x7C, 0x6C, 0x5C, 0xAC,
	0x0F, 0x8D, 0x62, 0xF8, 0x97, 0xC6, 0x95, 0x3D, 0xD1, 0x2F, 0x28, 0xB7,
	0x0C, 0x5B, 0x7D, 0xF7, 0x51, 0x81, 0x9A, 0x98, 0x34, 0x65, 0x26, 0x25,
	0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x03,
	0x70, 0x41, 0x38, 0xEF, 0xBB, 0xBD, 0xA1, 0x6A, 0x98, 0x7D, 0xD9, 0x01,
	0x32, 0x6D, 0x1C, 0x94, 0x59, 0x48, 0x4C, 0x88, 0xA2, 0x86, 0x1B, 0x91,
	0xA3, 0x12, 0x58, 0x7A, 0xE7, 0x0E, 0xF6, 0x23, 0x7E, 0xC5, 0x0E, 0x10,
	0x32, 0xDC, 0x39, 0xDD, 0xE8, 0x9A, 0x96, 0xA8, 0xE8, 0x59, 0xD7, 0x6A,
	0x98, 0xA6, 0xE7, 0xE3, 0x6A, 0x0C, 0xFE, 0x35, 0x2C, 0xA8, 0x93, 0x05,
	0x82, 0x34, 0xFF, 0x83, 0x3F, 0xCB, 0x3B, 0x03, 0x81, 0x1E, 0x9F, 0x0D,
	0xC0, 0xD9, 0xA5, 0x2F, 0x80, 0x45, 0xB4, 0xB2, 0xF9, 0x41, 0x1B, 0x67,
	0xA5, 0x1C, 0x44, 0xB5, 0xEF, 0x8C, 0xE7, 0x7B, 0xD6, 0xD5, 0x6B, 0xA7,
	0x57, 0x34, 0xA1, 0x85, 0x6D, 0xE6, 0xD4, 0xBE, 0xD6, 0xD3, 0xA2, 0x42,
	0xC7, 0xC8, 0x79, 0x1B, 0x34, 0x22, 0x37, 0x5E, 0x5C, 0x77, 0x9A, 0xBF,
	0x07, 0x2F, 0x76, 0x95, 0xEF, 0xA0, 0xF7, 0x5B, 0xCB, 0x83, 0x78, 0x9F,
	0xC3, 0x0E, 0x3F, 0xE4, 0xCC, 0x83, 0x92, 0x20, 0x78, 0x40, 0x63, 0x89,
	0x49, 0xC7, 0xF6, 0x88, 0x56, 0x5F, 0x64, 0x9B, 0x74, 0xD6, 0x3D, 0x8D,
	0x58, 0xFF, 0xAD, 0xDA, 0x57, 0x1E, 0x95, 0x54, 0x42, 0x6B, 0x13, 0x18,
	0xFC, 0x46, 0x89, 0x83, 0xD4, 0xC8, 0xA5, 0x62, 0x8B, 0x06, 0xB6, 0xFC,
	0x5D, 0x50, 0x7C, 0x13, 0xE7, 0xA1, 0x8A, 0xC1, 0x51, 0x1E, 0xB6, 0xD6,
	0x2E, 0xA5, 0x44, 0x8F, 0x83, 0x50, 0x14, 0x47, 0xA9, 0xAF, 0xB3, 0xEC,
	0xC2, 0x90, 0x3C, 0x9D, 0xD5, 0x2F, 0x92, 0x2A, 0xC9, 0xAC, 0xDB, 0xEF,
	0x58, 0xC6, 0x02, 0x18, 0x48, 0xD9, 0x6E, 0x20, 0x87, 0x32, 0xD3, 0xD1,
	0xD9, 0xD9, 0xEA, 0x44, 0x0D, 0x91, 0x62, 0x1C, 0x7A, 0x99, 0xDB, 0x88,
	0x43, 0xC5, 0x9C, 0x1F, 0x2E, 0x2C, 0x7D, 0x9B, 0x57, 0x7D, 0x51, 0x2C,
	0x16, 0x6D, 0x6F, 0x7E, 0x1A, 0xAD, 0x4A, 0x77, 0x4A, 0x37, 0x44, 0x7E,
	0x78, 0xFE, 0x20, 0x21, 0xE1, 0x4A, 0x95, 0xD1, 0x12, 0xA0, 0x68, 0xAD,
	0xA0, 0x19, 0xF4, 0x63, 0xC7, 0xA5, 0x56, 0x85, 0xAA, 0xBB, 0x68, 0x88,
	0xB9, 0x24, 0x64, 0x83, 0xD1, 0x8B, 0x9C, 0x80, 0x6F, 0x47, 0x49, 0x18,
	0x33, 0x17, 0x82, 0x34, 0x4A, 0x4B, 0x85, 0x31, 0x33, 0x4B, 0x26, 0x30,
	0x32, 0x63, 0xD9, 0xD2, 0xEB, 0x4F, 0x4B, 0xB9, 0x96, 0x02, 0xB3, 0x52,
	0xF6, 0xAE, 0x40, 0x46, 0xC6, 0x9A, 0x5E, 0x7E, 0x8E, 0x4A, 0x18, 0xEF,
	0x9B, 0xC0, 0xA2, 0xDE, 0xD6, 0x13, 0x10, 0x41, 0x70, 0x12, 0xFD, 0x82,
	0x4C, 0xC1, 0x16, 0xCF, 0xB7, 0xC4, 0xC1, 0xF7, 0xEC, 0x71, 0x77, 0xA1,
	0x74, 0x46, 0xCB, 0xDE, 0x96, 0xF3, 0xED, 0xD8, 0x8F, 0xCD, 0x05, 0x2F,
	0x0B, 0x88, 0x8A, 0x45, 0xFD, 0xAF, 0x2B, 0x63, 0x13, 0x54, 0xF4, 0x0D,
	0x16, 0xE5, 0xFA, 0x9C, 0x2C, 0x4E, 0xDA, 0x98, 0xE7, 0x98, 0xD1, 0x5E,
	0x60, 0x46, 0xDC, 0x53, 0x63, 0xF3, 0x09, 0x6B, 0x2C, 0x60, 0x7A, 0x9D,
	0x8D, 0xD5, 0x5B, 0x15, 0x02, 0xA6, 0xAC, 0x7D, 0x3C, 0xC8, 0xD8, 0xC5,
	0x75, 0x99, 0x8E, 0x7D, 0x79, 0x69, 0x10, 0xC8, 0x04, 0xC4, 0x95, 0x23,
	0x50, 0x57, 0xE9, 0x1E, 0xCD, 0x26, 0x37, 0xC9, 0xC1, 0x84, 0x51, 0x51,
	0xAC, 0x6B, 0x9A, 0x04, 0x90, 0xAE, 0x3E, 0xC6, 0xF4, 0x77, 0x40, 0xA0,
	0xDB, 0x0B, 0xA3, 0x6D, 0x07, 0x59, 0x56, 0xCE, 0xE7, 0x35, 0x4E, 0xA3,
	0xE9, 0xA4, 0xF2, 0x72, 0x0B, 0x26, 0x55, 0x0C, 0x7D, 0x39, 0x43, 0x24,
	0xBC, 0x0C, 0xB7, 0xE9, 0x31, 0x7D, 0x8A, 0x86, 0x61, 0xF4, 0x21, 0x91,
	0xFF, 0x10, 0xB0, 0x82, 0x56, 0xCE, 0x3F, 0xD2, 0x5B, 0x74, 0x5E, 0x51,
	0x94, 0x90, 0x6B, 0x4D, 0x61, 0xCB, 0x4C, 0x2E, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x52, 0x6F, 0x6F, 0x74,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x01, 0x43, 0x41, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30,
	0x30, 0x33, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7B, 0xE8, 0xEF, 0x6C,
	0xB2, 0x79, 0xC9, 0xE2, 0xEE, 0xE1, 0x21, 0xC6, 0xEA, 0xF4, 0x4F, 0xF6,
	0x39, 0xF8, 0x8F, 0x07, 0x8B, 0x4B, 0x77, 0xED, 0x9F, 0x95, 0x60, 0xB0,
	0x35, 0x82, 0x81, 0xB5, 0x0E, 0x55, 0xAB, 0x72, 0x11, 0x15, 0xA1, 0x77,
	0x70, 0x3C, 0x7A, 0x30, 0xFE, 0x3A, 0xE9, 0xEF, 0x1C, 0x60, 0xBC, 0x1D,
	0x97, 0x46, 0x76, 0xB2, 0x3A, 0x68, 0xCC, 0x04, 0xB1, 0x98, 0x52, 0x5B,
	0xC9, 0x68, 0xF1, 0x1D, 0xE2, 0xDB, 0x50, 0xE4, 0xD9, 0xE7, 0xF0, 0x71,
	0xE5, 0x62, 0xDA, 0xE2, 0x09, 0x22, 0x33, 0xE9, 0xD3, 0x63, 0xF6, 0x1D,
	0xD7, 0xC1, 0x9F, 0xF3, 0xA4, 0xA9, 0x1E, 0x8F, 0x65, 0x53, 0xD4, 0x71,
	0xDD, 0x7B, 0x84, 0xB9, 0xF1, 0xB8, 0xCE, 0x73, 0x35, 0xF0, 0xF5, 0x54,
	0x05, 0x63, 0xA1, 0xEA, 0xB8, 0x39, 0x63, 0xE0, 0x9B, 0xE9, 0x01, 0x01,
	0x1F, 0x99, 0x54, 0x63, 0x61, 0x28, 0x70, 0x20, 0xE9, 0xCC, 0x0D, 0xAB,
	0x48, 0x7F, 0x14, 0x0D, 0x66, 0x26, 0xA1, 0x83, 0x6D, 0x27, 0x11, 0x1F,
	0x20, 0x68, 0xDE, 0x47, 0x72, 0x14, 0x91, 0x51, 0xCF, 0x69, 0xC6, 0x1B,
	0xA6, 0x0E, 0xF9, 0xD9, 0x49, 0xA0, 0xF7, 0x1F, 0x54, 0x99, 0xF2, 0xD3,
	0x9A, 0xD2, 0x8C, 0x70, 0x05, 0x34, 0x82, 0x93, 0xC4, 0x31, 0xFF, 0xBD,
	0x33, 0xF6, 0xBC, 0xA6, 0x0D, 0xC7, 0x19, 0x5E, 0xA2, 0xBC, 0xC5, 0x6D,
	0x20, 0x0B, 0xAF, 0x6D, 0x06, 0xD0, 0x9C, 0x41, 0xDB, 0x8D, 0xE9, 0xC7,
	0x20, 0x15, 0x4C, 0xA4, 0x83, 0x2B, 0x69, 0xC0, 0x8C, 0x69, 0xCD, 0x3B,
	0x07, 0x3A, 0x00, 0x63, 0x60, 0x2F, 0x46, 0x2D, 0x33, 0x80, 0x61, 0xA5,
	0xEA, 0x6C, 0x91, 0x5C, 0xD5, 0x62, 0x35, 0x79, 0xC3, 0xEB, 0x64, 0xCE,
	0x44, 0xEF, 0x58, 0x6D, 0x14, 0xBA, 0xAA, 0x88, 0x34, 0x01, 0x9B, 0x3E,
	0xEB, 0xEE, 0xD3, 0x79, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

Xaml_SearchButton = """<Button xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" Content="Search" HorizontalAlignment="Left" Margin="10,10,0,0" VerticalAlignment="Top" Width="100"/>"""
Xaml_InputBox = """<TextBox xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:material="clr-namespace:MaterialDesignThemes.Wpf;assembly=MaterialDesignThemes.Wpf" TextWrapping="Wrap" material:HintAssist.Hint="Any text, keyword, name..." Margin="119,10,10,0" FontFamily="roboto" FontSize="14" Height="32" VerticalAlignment="Top"/>"""
Xaml_TitleData = """<ListBox xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" Margin="0,75,0,0" Background="#202020"/>"""
Xaml_InfoText = """<Label xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" HorizontalAlignment="Left" Foreground="White" FontFamily="roboto" FontSize="14" Margin="10,47,0,0" VerticalAlignment="Top"/>"""

cwd = dirname(realpath(argv[0]))
titlemeta = "http://3ds.titlekeys.gq/json_enc"
cdnurl = "http://nus.cdn.c.shop.nintendowifi.net/ccs/download/"
titleid = str()
titlekey = str()
name = str()
encname = str()
cia = str()
dir = cwd
tname = str()
region = str()
idx = int()
enctname = str()
vrs = str()
code = str()
db = None
lst = []


def __url(numblocks, blocksize, filesize, url = None):
    stdout.write("\b")
    amount = blocksize * numblocks
    if amount / 1024 < 1000: print( " - [Download] Progress: " + str(float(amount / 1024)) + " KB...", end="\r ")
    elif amount / 1024 >= 1000: print( " - [Download] Progress: " + str(float((amount / 1024) / 1024)) + " MB...", end="\r ")
    elif (amount / 1024) / 1024 >= 1000: print( " - [Download] Progress: " + str(float(((amount / 1024) / 1024) / 1024)) + " GB...", end="\r ")

def DownloadUrl(url, dst):
    if stdout.isatty(): urlretrieve(url, dst, lambda nb, bs, fs, url=url: __url(nb,bs,fs,url))
    else: urlretrieve(url, dst)
    print("- [Download] Finished!                                                      ")

def MakeCIA():
    global dir
    global cwd
    global titleid
    global titlekey
    global name
    global idx
    global cia
    global vrs
    global lst
    global db
    global region
    global tname
    global code
    global encname
    global enctname
    titleid = db[idx]["titleID"]
    titlekey = db[idx]["encTitleKey"]
    region = db[idx]["region"]
    code = db[idx]["serial"]
    tname = db[idx]["name"]
    name = tname + " [" + region + "]"
    encname = name.encode("ascii", errors="ignore").replace(":", "")
    enctname = tname.encode("ascii", errors="ignore")
    tregion = str()
    if "EUR" in region: tregion = "Europe (EUR)"
    elif "USA" in region: tregion = "North America (USA)"
    elif "JPN" in region: tregion = "Japan (JPN)"
    else: tregion = "Unknown"
    print("")
    print(" - [Download] Downloading title information:")
    print("")
    print("   =====================================================================")
    print(" - Title name: " + enctname)
    print(" - Region: " + tregion)
    print(" - Title ID: " + titleid)
    print(" - Code name: " + code)
    print(" - Encrypted Key: " + titlekey)
    print(" - Total size (MB): " + str(round((float(db[idx]["size"]) / 1024) / 1024, 2)) + " MB")
    print("   =====================================================================")
    print("")
    dir = cwd + "\\" + encname
    if exists(dir): rmtree(dir)
    mkdir(dir)
    print(" - [Download] Downloading TMD file...")
    tpg = urlopen(cdnurl + titleid + "/tmd")
    tmd = open(dir + "\\tmd", "wb")
    tmd.write(tpg.read());
    tmd.close()
    tmd = open(dir + "\\tmd", "rb")
    tmd.seek(0x140 + 0x9C)
    vrs = tmd.read(2)
    tmd.close()
    logp = Popen("\"" + cwd + "\\ctrtool.exe\" -t tmd -i \"" + dir + "\\tmd\"", stdout = PIPE)
    logdata = logp.stdout.read()
    cnts = str(logdata).count("Content id:             ")
    cntlst = []
    for i in str(logdata).splitlines():
        if "Content id:             " in i: cntlst.append(i[-8:])
    print(" - [Download] Downloading title's contents:")
    print("")
    print("   =====================================================================")
    for i in cntlst:
        print(" - Content name: " + i)
        DownloadUrl(cdnurl + titleid + "/" + i, dir + "\\" + i)
    print("   =====================================================================")
    print("")
    print(" - [Download] Generating Ticket file...")
    cetk = open(dir + "\\cetk", "wb")
    for i in range(0, 8): metacetk[0x140 + 0x9C + i] = titleid.decode("hex")[i]
    for i in range(0, 16): metacetk[0x140 + 0x7F + i] = titlekey.decode("hex")[i]
    for i in range(0, 2): metacetk[0x140 + 0xA6 + i] = vrs[i]
    cetk.write(bytearray(metacetk))
    cetk.close()
    print(" - [Download] Packing temporary files in a single CIA archive (" + cia  + ")...")
    ciap = Popen("\"" + cwd + "\\make_cdn_cia\" \"" + dir + "\" \"" + cia + "\"", stdout = PIPE)
    ciap.stdout.read()
    print(" - [Download] CIA archive successfully generated at: \"" + cia + "\"")
    if exists(dir): rmtree(dir)
    print("")
    print("   -------------------------------------------------------------------------------------------------------------------")
    print("")
    print(" - [System] Ready to download!")

class UI(MetroWindow):
    def AboutClick(self, s, e):
        MessageBox.Show("CDNTool downloader - version: beta 1 (v0.1)\nCopyright 2018: made by XorTroll developing.\n\nThis program allows you to download eShop titles as CIA archives.\nThis program DOES NOT access eShop's title database.\nIt accesses another one, which is displayed in the prompt.\n\nData accessed from the database is not always correct, because\nit is open-source and anybody can submit data there.\n\nThis program uses external tools and libraries.\n\nList of used tools:\n - Material Design in XAML .NET library [for WPF]\n - MahApps.Metro .NET library [for WPF]\n - ctrtool executable\n - make_cdn_cia executable\n\nDeveloped using Python 2.7.14, with .NET Framework support\nThis beautiful Material & Metro style was made using WPF\nwith the libraries mentioned above (isn't it beautiful?)", "About CDNTool downloader")
    def TitleSelect(self, s, e):
        global dir
        global cwd
        global titleid
        global titlekey
        global name
        global idx
        global cia
        global vrs
        global lst
        global db
        global region
        global tname
        global code
        global encname
        global enctname
        if self._TitleData.SelectedItem is not None:
            t = str()
            idx = lst[self._TitleData.SelectedIndex]
            txt = "Selected title: " + db[idx]["name"]
            txt += "\nCodename: " + db[idx]["serial"]
            if "EUR" in db[idx]["region"]: t = "Europe (EUR)"
            elif "USA" in db[idx]["region"]: t = "North America (USA)"
            elif "JPN" in db[idx]["region"]: t = "Japan (JPN)"
            else: t = "Unknown"
            txt += "\nRegion: " + t
            txt += "\nTotal size: " + str(round((float(db[idx]["size"]) / 1024) / 1024, 2)) + " MB"
            txt += "\n\nDo you want to download this title?"
            result = MessageBox.Show(txt, "CDNTool - download confirmation", MessageBoxButtons.YesNo)
            if result is not DialogResult.Yes:
                self._TitleData.SelectedItem = None
                return
            tname = db[idx]["name"]
            sfd = SaveFileDialog()
            sfd.Filter = "CTR Importable Archive (*.cia)|*.cia|Any kind of file|*.*"
            sfd.Title = "Downloading as CIA archive: " + tname
            sfd.ShowDialog()
            cia = sfd.FileName
            if cia is "" or cia is None or len(cia) is 0:
                self._TitleData.SelectedItem = None
                return
            tcia = Thread(ThreadStart(MakeCIA))
            tcia.SetApartmentState(ApartmentState.STA)
            tcia.Start()
            tcia.Join()
            self._InfoText.Content = "Downloaded successfully: " + cia
        else:
            self._TitleData.SelectedItem = None
            return
            
    def SearchClick(self, s, e):
        global dir
        global cwd
        global titleid
        global titlekey
        global name
        global idx
        global cia
        global vrs
        global lst
        global db
        global region
        global tname
        global code
        global encname
        global enctname
        lst = []
        self._TitleData.Items.Clear()
        inpt = self._InputBox.Text
        id = 0
        fnd = 0
        for i in db:
            if inpt.lower() in i["name"].encode("ascii", errors="ignore").lower():
                fnd += 1
                lst.append(id)
            id += 1
        self._InfoText.Content = "Found: " + str(len(lst)) + " titles."
        for i in lst:
            txt = db[i]["name"]
            if "EUR" in db[i]["region"]: txt += " [Europe]"
            elif "USA" in db[i]["region"]: txt += " [North America]"
            elif "JPN" in db[i]["region"]: txt += " [Japan]"
            else: txt += " [Unknown region]"
            self._TitleData.Items.Add(txt)
    def __init__(self):
        clr = Button()
        clr.Content = "About"
        clr.Click += self.AboutClick
        cmds = WindowCommands()
        cmds.Items.Add(clr)
        self.RightWindowCommands = cmds
        self.WindowTitleBrush = BrushColor("#000033")
        self.Background = BrushColor("#000040")
        self.NonActiveWindowTitleBrush = BrushColor("#000040")
        self.TitleTemplate = XamlTitleTemplate("CDNTool downloader - UI")
        self.Resources = XamlObject(Xaml_Dicts)
        self.Width = Xaml_Width
        self.Height = Xaml_Height
        self.Title = "CDNTool downloader - UI"
        self._Container = Grid()
        self._SearchButton = XamlObject(Xaml_SearchButton)
        self._SearchButton.Click += self.SearchClick
        self._SearchButton.ToolTip = "Click to search (if input text is empty all the list will be shown)"
        self._Container.Children.Add(self._SearchButton)
        self._InputBox = XamlObject(Xaml_InputBox)
        self._Container.Children.Add(self._InputBox)
        self._TitleData = XamlObject(Xaml_TitleData)
        self._TitleData.SelectionChanged += self.TitleSelect
        self._Container.Children.Add(self._TitleData)
        self._InfoText = XamlObject(Xaml_InfoText)
        self._InfoText.Content = "Found: " + str(len(db)) + " titles stored."
        self._Container.Children.Add(self._InfoText)
        self.Content = self._Container

def Main():
    while True:
        print("")
        print(" - [System] Loading CDNTool UI...")
        print("")
        print("   -------------------------------------------------------------------------------------------------------------------")
        print("")
        print(" - [System] Ready to download!")
        wnd = UI()
        wnd.ShowDialog()
        print("")
        print(" - [System] UI closed. Press any key to reopen it.")
        print(" - [System] You can close this prompt after closing the UI to close CDNTool.", end="")
        system("pause > nul 2> nul")
        print("")

# Entrypoint for CDNTool, both prompt and UI
    
system("title CDNTool downloader - prompt")
ShowWindow(GetConsoleWindow(), 3)
print("")
print("  **  CDNTool prompt  **")
print("")
print(" - [About] Current version: beta 1 (v0.1)")
print(" - [About] Copyright (C) 2018: made by XorTroll developing")
print("")
print(" - [System] You will see here the download progress of the titles.")
print("")
print(" - [Warning] During download the UI usually freezes, but the program is still working (if this window")
print("             still works), so don't close the UI, because it would close the entire program.")
print("")
print("")
print(" - [System] Downloading (unofficial) title database: " + titlemeta)
try:
    pg = urlopen(titlemeta)
except:
    ErrorMessage("CDNTool downloader - Database error", "Error accessing title database.\nDo you have internet connection, or is the page OK?")
print("")
DownloadUrl(titlemeta, dir + "\\.titledata")
fdb = open(dir + "\\.titledata")
db = loads(fdb.read())
fdb.close()
unlink(dir + "\\.titledata")

t = Thread(ThreadStart(Main))
t.SetApartmentState(ApartmentState.STA)
t.Start()
t.Join()