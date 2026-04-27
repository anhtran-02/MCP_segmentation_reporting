name: report_content
description: call these function to get data, query and get metrics to generate reports.
--------



def team_over_view():
    # 1. metrics:
    - total campaign, total segment, total creators campaign, average condition per segment

    2. dimension
    - overall across the timerange (e.g. quarter 1.2026)
    - break by channel
    - break by channel and goal

def condition_analysis:
  # what drives audience selection?
  - Top condition order by campaign count
  - top condition is use, give insight based on condition_name
  - Core audience pool - base on segment name to detect the target segment
  - number of CDP attribute vs. BQ condition used in created segment, which attribute_name or condition_name is top use?
  - other underutilized behavioural signal that can recommend.


def size_pool_distribution()
  """
  Analyze size pool (segment size) to enhance personalization in campaign trigger.
  """
  - use median size pool instead of average size pool.
  - median size pool by goal
  - median size pool for each channel
  - give insight or recommendation base on size pool
  - If one segment have multiple size pool value, take the latest one to report

def tactics_per_creator:
  """
  Give profile for creators
  Analyse tactic of the BU used segment or creator (use column created_by) based on their behavioural.
  """

  - total campapinsm, avg condition per segment, mix ratio between conditions and attributes used, reused segments in campaigns.
  - based on their behaviours to categorized and label them into groups
  - give short comment on their behavior, give them more use case to use segment and campaign, in order to enhance the campaign performance and achive their KPI. 

def segment_health_quality:
  """
  segment good if:
  - high num of attribute is used more than conditions.
  - same segment tactics should be reused instead of generated multiple time repeatedly without extend tactics -> optimize cost.
  - segment created should be used instead of redundant -> optimize cost.
  - segment has specific tactics instead of use mass.
  - segment has proficient description and naming consistent to analyse and reuse if needed.
  - segment trigger campaign and gain good campaign performance (impression, click, ctr)
  """

def condition_attribute_health:
  """
  condition or attribute is good if:
  - they are used at least one in last 90 days.
  - more attributes are used compare to conditions in each segments
  """

def summarize recommendation:
  """
  Summarize insights and recommendations for the report
  """
  - Any bad cases should be concerned.
  - Any good tactics should enhance and improve.
  For each insight and recommendation, should include:
  - header
  - short insight, short example
  - scope
  - impact
