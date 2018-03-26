import glob
import sys
from dateparser import parse
import datetime
from pyquery import PyQuery


# Change this to your name!
my_name = 'Eric Wadkins'


# Configuration
parse_date = False # Unnecessary and significantly increases processing time
output_progress = True
conversation_files = glob.glob('messages/*.html')

def parse_conversation_file(filepath, parse_date=True, conversation_name_callback=None, output_progress=False):
    with open(filepath) as f:
        pq = PyQuery(f.read())
        pq('.warning').parent().remove()
        conversation_name = pq('title').text()
        if conversation_name_callback:
            conversation_name_callback(conversation_name)
        participants = pq('div.thread').text().split('\n')[1].replace('Participants: ', '')
        messages = []
        elements = list(pq('div.thread > div.message, div.thread > p').items())
        progress_bar_size = 60
        for i in range(0, len(elements), 2):
            if output_progress and ((i/2+1) % 50 == 0 or i == 0):
                progress_bar = '['
                progress_bar += '#' * int(float(i/2+1) / (len(elements)/2) * progress_bar_size)
                progress_bar += ' ' * (progress_bar_size - len(progress_bar) + 1)
                progress_bar += ']'
                sys.stdout.write('\r' + progress_bar + ' ' + str(i/2+1) + '/' + str(len(elements)/2) + ' ')
                sys.stdout.flush()
            date = elements[i].find('.meta').text()
            if parse_date:
                date = parse(date)
            messages.append((date,
                             elements[i].find('.user').text(),
                             str(elements[i+1]).replace('<p>', '').replace('</p>', '').replace('<p/>', '')))
        if output_progress:
            sys.stdout.write('\r')
            sys.stdout.write(' ' * (progress_bar_size + 16))
            sys.stdout.write('\r')
            sys.stdout.flush()
    return conversation_name, participants, list(reversed(messages))

def load_stop_words(filepath):
    with open(filepath) as f:
        content = [x.strip() for x in f.readlines()]
        return set([x for x in content if x])
    

# Data loading and parsing
conversations = []
for i in range(len(conversation_files)):
    sys.stdout.write('[' + str(i+1) + '/' + str(len(conversation_files)) +'] '
                     + 'Parsing ')
    sys.stdout.flush()
    def conversation_name_callback(conversation_name):
        sys.stdout.write(conversation_name + '..\n')
        sys.stdout.flush()
    conversation_name, participants, messages = \
        parse_conversation_file(conversation_files[i],
                                parse_date=parse_date,
                                conversation_name_callback=conversation_name_callback,
                                output_progress=output_progress)
    conversations.append((conversation_name, participants, messages))
print

#stop_words = load_stop_words('english_stop_words.txt')
#stop_words = stop_words | set(map(lambda w: w.replace('\'', ''), stop_words))
stop_words = set(['all', 'whys', "when's", 'with', 'should', 'to', 'only', 'under', 'do', 'his', 'very', "they'd", 'cannot', 'werent', 'during', 'him', "we'll", 'did', "they've", 'these', 'she', "won't", 'havent', 'where', "i'll", "you'd", 'whens', 'up', 'are', 'further', 'what', 'heres', "there's", 'above', 'between', 'youll', 'we', 'here', 'hers', "aren't", 'both', 'didnt', "wouldn't", 'wed', 'against', "i'd", "weren't", "i'm", "can't", 'thats', "hadn't", "couldn't", 'from', 'would', "it's", 'been', 'whos', 'whom', 'themselves', 'until', 'more', 'on', "what's", 'mustnt', 'those', 'me', 'myself', 'theyve', 'this', 'while', 'ought', 'of', 'my', 'ill', 'theres', 'ive', 'is', "didn't", 'it', 'cant', 'itself', 'im', 'in', 'id', 'if', 'same', 'how', 'arent', 'shouldnt', 'after', 'such', "he'll", 'wheres', 'a', 'hows', 'off', 'i', 'youre', 'well', 'so', 'the', 'yours', "that's", "she'll", "don't", 'being', 'over', 'isnt', 'through', 'yourselves', 'hell', 'its', 'before', "he's", "we've", 'had', "he'd", 'lets', 'ours', 'has', "haven't", 'then', 'them', "who's", "you've", 'they', 'not', 'nor', 'wont', 'theyre', 'each', "mustn't", "isn't", "why's", 'weve', 'because', 'doing', 'some', "we'd", 'our', 'ourselves', 'out', 'for', 'does', "shouldn't", "they'll", 'be', "you're", 'by', "where's", 'about', 'wouldnt', 'theirs', 'could', 'hes', 'youve', 'or', 'own', 'whats', 'dont', 'into', 'youd', 'shed', 'yourself', 'down', 'doesnt', 'theyd', 'couldnt', 'your', "doesn't", "how's", 'her', 'few', 'there', 'hed', 'their', 'too', 'was', "we're", 'himself', "i've", 'but', 'hadnt', 'shant', 'herself', 'than', "here's", 'he', "they're", "wasn't", "hasn't", 'below', 'were', 'shes', 'and', 'wasnt', 'am', 'an', 'as', 'shell', 'at', 'have', 'any', 'again', 'hasnt', 'theyll', 'no', 'that', 'when', 'other', 'which', 'you', "shan't", 'who', "let's", 'most', 'why', "she'd", "you'll", "she's", 'having', 'once'])

# Helper functions
def print_conversation(conversation):
    conversation_name, participants, messages = conversation
    print 'Title:', conversation_name
    print
    print 'Participants (' + str(len(participants.split(','))) + '):', participants
    print
    print 'Messages (' + str(len(messages)) + ')'
    for (date, user, message) in messages:
        date_string = (('(' + date.strftime("%m/%d/%y %I:%M%p") + ') ') if isinstance(date, datetime.date) else '')
        print date_string + \
            user + ':', message

def me_filter(m):
    return m[1] == my_name

print 'Top 20 conversations by number of messages sent in total'
conversations.sort(key=lambda c: -len(c[2]))
for conversation in conversations[:20]:
    print len(conversation[2]), '\t' + conversation[0]
print '...'
print

print 'Top 20 conversations by number of messages sent by you'
tmp = list(conversations)
tmp.sort(key=lambda c: -len(filter(me_filter, c[2])))
for conversation in tmp[:20]:
    print len(filter(me_filter, conversation[2])), '\t' + conversation[0]
print '...'
print

print 'Top 20 words most frequently used by you (excluding stop words)'
all_messages = [item for sublist in map(lambda c: c[2], conversations) for item in sublist]
all_messages_by_me = filter(me_filter, all_messages)
words = [item for sublist in map(lambda m: m[2].split(), all_messages_by_me) for item in sublist]
words = map(lambda w: w.lower(), words)
word_count_map = {}
for word in words:
    word_count_map[word] = word_count_map.get(word, 0) + 1
words = list(set(words) - stop_words)
words.sort(key=lambda w: -word_count_map[w])
for word in words[:20]:
    print word_count_map[word], '\t' + word
print '...'
print

print 'Top 20 most lopsided conversations (sent/received ratio of one-on-one conversations with more than 50 messages)'
tmp = list(conversations)
tmp = filter(lambda c: len(c[1].split(',')) == 1 and len(c[2]) > 50, tmp)
unevenness_map = {}
sent_received_ratio_map = {}
for conversation in tmp:
    sent_by_me = filter(me_filter, conversation[2])
    sent_received_ratio = float(len(sent_by_me)) / (max(0.00000001, len(conversation[2]) - len(sent_by_me)))
    unevenness = abs(1.0 - sent_received_ratio)
    unevenness_map[conversation[0]] = unevenness
    sent_received_ratio_map[conversation[0]] = sent_received_ratio
tmp.sort(key=lambda c: -unevenness_map[c[0]])
for conversation in tmp[:20]:
    print sent_received_ratio_map[conversation[0]], '\t' + conversation[0]
print

print 'Total number of messages sent by you'
print len(all_messages_by_me)
print
        
#for conversation in conversations:
#    print_conversation(conversation)