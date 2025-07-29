# wagtail-places

This app was mainly created to easily add multiple locations to a page in a Wagtail site.

This can be useful to improve SEO, show locations of your business on a map, etc.

## Example Use Case

A client has a single store, but ships/does work across multiple cities.

The store will likely only show up if someone searches the name of the store, or a related keyword and the location/city name of where the store is located.  
Let's say the store is located in New York, but the client also ships to Los Angeles, Chicago, and Miami.

When someone searches for `"<keyword> in Los Angeles"`, the client's store will not show up in the search results, because the store is located in New York.

We aim to improve this by allowing a list of locations to be added to a `PlacesPage`, so that when someone searches for `"<keyword> in Los Angeles"`, the client's store will show up in the search results.

In short, the goal is to add a "place" for each city the client ships to, and the client's store will show up in the search results for each of those cities.

## Quick start

1. Install the package via pip:

   ```bash
   pip install wagtail-places
   ```

2. Add 'places' to your INSTALLED_APPS setting like this:

   ```python
   INSTALLED_APPS = [
   ...,
      'places',
   ]
   ```

3. Go to the pages section in the Wagtail admin and create a new page with the 'Places' page type.
