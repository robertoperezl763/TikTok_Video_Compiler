from datetime import timedelta
import re

# Helper function to convert SRT time format to timedelta
def srt_time_to_timedelta(srt_time):
    hours, minutes, seconds = map(float, re.split('[:,]', srt_time))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

# Helper function to convert timedelta to SRT time format
def timedelta_to_srt_time(td):
    total_seconds = int(td.total_seconds())
    milliseconds = int((td.total_seconds() - total_seconds) * 1000)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# Main function to split segments based on max word count
def split_text_into_segments(text, max_words):
    words = text.split()
    return [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

# Helper function to adjust timing
def adjust_time_segments(start_time, end_time, num_segments):
    start_td = timedelta(seconds=start_time)
    end_td = timedelta(seconds=end_time)
    total_duration = end_td - start_td
    segment_duration = total_duration / num_segments

    time_segments = []
    for i in range(num_segments):
        new_start_time = start_td + i * segment_duration
        new_end_time = new_start_time + segment_duration
        time_segments.append((new_start_time.total_seconds(), new_end_time.total_seconds()))
    return time_segments

# Main function to split JSON segments
def split_json_segments(json_data, max_words_per_segment):
    new_segments = []
    segment_counter = 0

    for segment in json_data:
        # Extract details from JSON
        segment_id = segment['id']
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']

        # Split text based on max word count
        text_segments = split_text_into_segments(text, max_words_per_segment)
        num_segments = len(text_segments)

        # Adjust timings based on the number of new segments
        time_segments = adjust_time_segments(start_time, end_time, num_segments)

        # Create new segments with updated timing and text
        for i, (new_text, (new_start, new_end)) in enumerate(zip(text_segments, time_segments)):
            new_segment = {
                'id': segment_counter,
                'start': new_start,
                'end': new_end,
                'text': new_text
            }
            new_segments.append(new_segment)
            segment_counter += 1

    return new_segments

# Function to convert seconds to SRT time format with millisecond precision
def format_time(seconds):
    td = timedelta(seconds=seconds)
    # print(f"this is the td display: {td}")
    
    if len(str(td)) <= 7:
        time_str = str(td) + ',000'
        return time_str
    else:
        time_str = str(td)[:-3]  # Remove microseconds part and keep milliseconds
        
    # print(f"this is timedelta display after: {time_str}")
    if '.' not in time_str:
        time_str += ',000'  # If there's no fractional part, add ',000' for milliseconds
    else:
        time_str = time_str.replace('.', ',')  # Replace '.' with ',' for SRT format

    # print(f"this is final format timestr: {time_str}")
    return time_str

# Revised function for formatting the JSON segments into SRT format with millisecond precision
def format_srt_segments(segments, fileLocation: str):
    formatted_segments = []
    
    for segment in segments:
        # Convert start and end times with millisecond precision
        start_time = str(0)+format_time(segment['start'])
        end_time = str(0)+format_time(segment['end'])
        text = segment['text']
        segment_id = segment['id'] + 1  # SRT IDs are 1-based
        
        # Create the formatted SRT segment
        formatted_segment = f"{segment_id}\n{start_time} --> {end_time}\n{text.strip()}\n\n"
        # formatted_segments.append(formatted_segment)

        with open(fileLocation, 'a', encoding='utf-8') as file:
            file.write(formatted_segment)
    
    return fileLocation
