from shiny import App, render, ui, reactive
import traceback
from Solver import *


app_ui = ui.page_fluid(
  ui.h2("Spelling Bee Solver"),
  ui.input_text(id='puzzle', label='Puzzle (center letter first):', value='manitob', placeholder='abcdefg (center letter first)'),
  ui.input_action_button("solveit", "Solve Puzzle!", class_="btn-success"),
  ui.div("This may take a few seconds."),
  ui.h3("Pangrams"),
  ui.output_text("pangrams"),
  ui.h3("Solutions"),
  ui.output_table("table"),
)


def server(input, output, session):
  @reactive.Calc
  @reactive.event(input.solveit, ignore_none=False)
  def getAllFoundWords():
    puzzleValue = input.puzzle()
    try:
      allFoundWords = solvePuzzle(puzzleValue)
      return allFoundWords
    except Exception as e:
      exceptionData = traceback.format_exc().splitlines()[-2:]
      ui.notification_show("\n".join(exceptionData), duration=None)
      raise e

  @output
  @render.table
  def table():
    return convertToDF(getAllFoundWords())

  @output
  @render.text
  @reactive.event(input.solveit, ignore_none=False)
  def pangrams():
    foundPangrams = findPangrams(puzzleValue=input.puzzle(), allFoundWords=getAllFoundWords())
    return "\n".join(foundPangrams)


app = App(app_ui, server)
