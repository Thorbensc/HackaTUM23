class LogChunker:
    def __init__(self) -> None:
        pass

    def split_context(self, context) -> list:
        context = context.splitlines()
        chunks = []
        start = 0
        maxChunkLength = 512
        #maxLineLength = max(context.splitlines(), key=len)
        shortLines = list(filter(lambda line: len(line) <= maxChunkLength, context))
        print("lines with less than 513 chars: ", len(list(shortLines)))
        #print("maxLineLength: " , (maxLineLength))

        while start < len(shortLines):
            chunk = ""
            
            # you need the -2 here, because 'n\' gets added to the chunk as well'
            while len(chunk) <= maxChunkLength-2 and start < len(shortLines):
                if(len(chunk) + len(shortLines[start])) <= maxChunkLength-2:
                    chunk += shortLines[start]
                    chunk += '\n'
                    start += 1
                else:
                    break
            chunks.append(chunk)
        return chunks

    def filter_error_chunks(self, chunks):
        keywords = ["error", "failure", "warning", "not found", "missing", "problem"]
        return [chunk for chunk in chunks if any(keyword in chunk for keyword in keywords)]