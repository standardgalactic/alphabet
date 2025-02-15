import datetime

# Quotes for alternating days
quote_1 = """\
**Holistic Understanding**

> Holistic understanding demands that we give the machine everything we have. Filtering or cleaning input data can lead to confusion in real-life scenarios. To enable true understanding, we should avoid heavy-handed heuristic cleanup of the input data.
>
>— 𝘔𝘰𝘯𝘪𝘤𝘢 𝘈𝘯𝘥𝘦𝘳𝘴𝘰𝘯
>
> Read more: [The Red Pill of Machine Learning](https://experimental-epistemology.ai/the-red-pill-of-machine-learning/)
"""

quote_2 = """\
**The Bitter Lesson**

> Faking intelligence is intelligence.  
> You can only fake it if you have it.  
>
>— 𝘑𝘶𝘥𝘦𝘢 𝘗𝘦𝘢𝘳𝘭
>
> For more information see: [Causal Reasoning and Counterfactuals](https://www.youtube.com/watch?v=pEBI0vF45ic)
"""

# Determine the quote based on the day's parity
today = datetime.datetime.now().day  # Get day of the month (1-31)
quote_of_the_day = quote_1 if today % 2 == 0 else quote_2  # Even days = quote_1, Odd days = quote_2

# Read current README content
with open("README.md", "r", encoding="utf-8") as file:
    readme_content = file.readlines()

# Define updated markers
start_marker = "<!-- START_QUOTE -->"
custom_marker = "<!-- Dual-Wave Encoding -->"
end_marker = "<!-- END_QUOTE -->"

# Replace the existing quote section
new_content = []
inside_quote_section = False

for line in readme_content:
    if start_marker in line:
        inside_quote_section = True
        new_content.append(line)
        new_content.append(custom_marker + "\n")  # Preserve your custom marker
        new_content.append("\n" + quote_of_the_day + "\n")  # Insert new quote
        continue
    if end_marker in line:
        inside_quote_section = False
    if not inside_quote_section:
        new_content.append(line)

# Write the updated README
with open("README.md", "w", encoding="utf-8") as file:
    file.writelines(new_content)

