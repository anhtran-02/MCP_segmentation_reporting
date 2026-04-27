name: BU-segmentation report
definition: define functions for calling report for each BU
----------------------
Rule:
- If there is any error when calling the mcp, return error reason and print to user.


@mcp.tool()
def list_bu_name():
    """
    List all BU names available across all datasets (or a specific one).
    Ask user specific dimension: SEGMENT, ATTRIBUTE, CONDITION, CAMPAIGN or ALL of them, then choose the right table to query created_by_department.
    """

def preview_bu_report(bu_name: str):
    """
    Preview report data for one BU without generating the PowerPoint.
    Use this to inspect KPIs, top conditions, issues, and recommendations first.
    After show the BU report as text on the chat UI, ask user do they want to generate a slide html? Yes (generate html slide) / No
    """
    - return information about report content that user define at the start of the conversation

def generate_slide_bu_report(bu_name: str):
    """
    Generate a html segmentation report for one BU from the database.
    After sucessfully generate, guide user how to download it if they want.
    """

def generate_slide_bu_report(bu_name: str):
    """
    Generate a html segmentation report for one BU from the database.
    After sucessfully generate, guide user how to download it if they want.
    """


def executive_summary(bu_name: str) -> str:
    """
    Concise 5-line executive summary card for a BU.
    """
    Call: preview_bu_report(bu_name="{bu_name}")

    Then respond with exactly this 5-line card (no extra text):

    BU: {bu_name} | period=<period> | campaigns=<N> | segments=<N> | operators=<N>
    reuse_ratio=<campaigns/segments rounded to 2dp> | avg_cond_per_seg=<X> | top_condition=<NAME> (<N> uses)
    issues_flagged=<count of issues>
    top_recommendation=<first recommendation verbatim>
    verdict=<one sentence: health rating and single most important action>

    Rules:
    - Compute reuse_ratio = total_campaigns / total_segments, round to 2 decimal places
    - issues_flagged = length of the issues list
    - No markdown headers, no extra lines, exactly 5 lines"""
