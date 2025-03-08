import json

class ApiScraperPipeline:
    def process_item(self, item, spider):
        # Save data to a JSON file (you can also save to a database if desired)
        with open('api_data.json', 'a') as f:
            json.dump(dict(item), f)
            f.write('\n')
        return item



# class NormalizeApiDocsPipeline:
#     def process_item(self, item, spider):
#         """Normalize API endpoint data."""
#         # Clean and normalize data here, e.g., removing unwanted characters, handling missing fields.
#         item['description'] = ' '.join(item['description']).strip()
#         item['schemas'] = [schema.strip() for schema in item['schemas']]
#
#         # Return normalized item
#         return item
#
#
# class SaveToJsonPipeline:
#     def open_spider(self, spider):
#         """Open a JSON file to save the scraped data."""
#         self.file = open('api_docs.json', 'w')
#
#     def close_spider(self, spider):
#         """Close the JSON file."""
#         self.file.close()
#
#     def process_item(self, item, spider):
#         """Write the item to JSON."""
#         line = json.dumps(dict(item)) + "\n"
#         self.file.write(line)
#         return item
