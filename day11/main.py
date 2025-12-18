from functools import lru_cache
import sys
from collections import deque

def find_all_paths(graph, start, end):
   """Optimized iterative DFS using stack instead of recursion"""
   paths = []
   stack = [(start, [start])]
   while stack:
      node, path = stack.pop()
      if node == end:
         paths.append(path)
         continue
      if node not in graph:
         continue
      path_set = set(path)  # O(1) lookup instead of O(n) list
      for neighbor in graph[node]:
         if neighbor not in path_set:
            stack.append((neighbor, path + [neighbor]))
   return paths

def find_all_paths_with_must_visit(graph, start, end, must_visit, path=None, _memo=None):
         if _memo is None:
            _memo = {}
         if path is None:
            path = []
         path_tuple = tuple(path + [start])
         memo_key = (start, end, path_tuple, tuple(sorted(must_visit)))
         if memo_key in _memo:
            return _memo[memo_key]
         path = path + [start]
         must_visit_remaining = [node for node in must_visit if node not in path]
         if start == end:
            if not must_visit_remaining:
               _memo[memo_key] = [path]
               return [path]
            else:
               _memo[memo_key] = []
               return []
         if start not in graph:
            _memo[memo_key] = []
            return []
         paths = []
         for node in graph[start]:
            if node not in path:
               newpaths = find_all_paths_with_must_visit(graph, node, end, must_visit_remaining, path, _memo)
               for newpath in newpaths:
                  paths.append(newpath)
         _memo[memo_key] = paths
         return paths

def build_reverse_graph(graph):
   """Build a reverse graph where edges point backwards"""
   reverse_graph = {}
   all_nodes = set(graph.keys())
   for node in graph:
      for neighbor in graph[node]:
         all_nodes.add(neighbor)
         if neighbor not in reverse_graph:
            reverse_graph[neighbor] = []
         reverse_graph[neighbor].append(node)
   return reverse_graph

def can_reach_target(graph, target):
   """Returns set of all nodes that can reach target using reverse BFS - O(V+E)"""
   # Build reverse graph
   reverse_graph = build_reverse_graph(graph)
   
   # BFS from target backwards
   reachable = {target}
   queue = deque([target])
   while queue:
      node = queue.popleft()
      if node in reverse_graph:
         for prev_node in reverse_graph[node]:
            if prev_node not in reachable:
               reachable.add(prev_node)
               queue.append(prev_node)
   return reachable

def nodes_reachable_from(graph, start):
   """Returns set of all nodes reachable from start using BFS - O(V+E)"""
   reachable = {start}
   queue = deque([start])
   while queue:
      node = queue.popleft()
      if node in graph:
         for neighbor in graph[node]:
            if neighbor not in reachable:
               reachable.add(neighbor)
               queue.append(neighbor)
   return reachable

def find_paths_optimized(graph, start, end, valid_nodes):
   """Count paths instead of storing them - much faster for large graphs"""
   # Use memoization with frozenset of visited nodes
   memo = {}
   
   def count_paths(node, visited_frozenset):
      if node == end:
         return 1
      if node not in graph:
         return 0
      
      memo_key = (node, visited_frozenset)
      if memo_key in memo:
         return memo[memo_key]
      
      count = 0
      for neighbor in graph[node]:
         if neighbor not in visited_frozenset and neighbor in valid_nodes:
            new_visited = visited_frozenset | frozenset([neighbor])
            count += count_paths(neighbor, new_visited)
      
      memo[memo_key] = count
      return count
   
   return count_paths(start, frozenset([start]))

def find_paths_reverse(graph, start, end, valid_nodes):
   """Count paths by searching from end to start in reverse graph - DAG optimized"""
   reverse_graph = build_reverse_graph(graph)
   
   # Check if graph is a DAG and use topological sort if so
   def topological_sort_and_count():
      # Filter to only valid nodes between start and end
      # Use DP: paths[node] = number of paths from node to end (svr)
      paths_count = {}
      paths_count[end] = 1  # Base case: 1 path from svr to svr
      
      # BFS to find all nodes on paths from start to end in reverse graph
      reachable_from_start = {start}
      queue = deque([start])
      while queue:
         node = queue.popleft()
         if node in reverse_graph:
            for neighbor in reverse_graph[node]:
               if neighbor not in reachable_from_start and neighbor in valid_nodes:
                  reachable_from_start.add(neighbor)
                  queue.append(neighbor)
      
      # Topological sort using Kahn's algorithm on the subgraph
      in_degree = {node: 0 for node in reachable_from_start}
      for node in reachable_from_start:
         if node in reverse_graph:
            for neighbor in reverse_graph[node]:
               if neighbor in reachable_from_start:
                  in_degree[neighbor] = in_degree.get(neighbor, 0) + 1
      
      queue = deque([node for node in reachable_from_start if in_degree[node] == 0])
      topo_order = []
      while queue:
         node = queue.popleft()
         topo_order.append(node)
         if node in reverse_graph:
            for neighbor in reverse_graph[node]:
               if neighbor in reachable_from_start:
                  in_degree[neighbor] -= 1
                  if in_degree[neighbor] == 0:
                     queue.append(neighbor)
      
      # If topo_order doesn't include all nodes, there's a cycle - fall back to DFS
      if len(topo_order) != len(reachable_from_start):
         return None  # Has cycles
      
      # DP: count paths in reverse topological order
      for node in reversed(topo_order):
         if node == end:
            continue
         paths_count[node] = 0
         if node in reverse_graph:
            for neighbor in reverse_graph[node]:
               if neighbor in paths_count:
                  paths_count[node] += paths_count[neighbor]
      
      return paths_count.get(start, 0)
   
   result = topological_sort_and_count()
   if result is not None:
      return result
   
   # Fall back to DFS with memoization if there are cycles
   memo = {}
   def count_paths(node, visited_frozenset):
      if node == end:
         return 1
      if node not in reverse_graph:
         return 0
      
      memo_key = (node, visited_frozenset)
      if memo_key in memo:
         return memo[memo_key]
      
      count = 0
      for neighbor in reverse_graph[node]:
         if neighbor not in visited_frozenset and neighbor in valid_nodes:
            new_visited = visited_frozenset | frozenset([neighbor])
            count += count_paths(neighbor, new_visited)
      
      memo[memo_key] = count
      return count
   
   return count_paths(start, frozenset([start]))

def main():
   servers = {}
   with open("input.txt") as f:
      for line in f:
         tmp = line.strip().split(": ")
         servers[tmp[0]] = [x for x in tmp[1].split(" ")]

   #part 1
   all_paths = find_all_paths(servers, "you", "out")
   print(len(all_paths))

   #part 2
   # Find paths from svr to out, going through both dac and fft (in any order)
   # Strategy: count paths for both orderings and sum them
   # Path 1: svr -> dac -> fft -> out
   # Path 2: svr -> fft -> dac -> out
   
   # For DAG: paths(svr->dac->fft->out) = paths(svr->dac) * paths(dac->fft) * paths(fft->out)
   # But we need to avoid counting paths that reuse nodes
   
   # Simpler approach: use the topological DP for each segment
   nodes_from_svr = nodes_reachable_from(servers, "svr")
   nodes_reaching_out = can_reach_target(servers, "out")
   valid_nodes = nodes_from_svr & nodes_reaching_out  # Nodes on paths from svr to out
   
   # Count paths: svr -> dac -> fft -> out
   paths_svr_dac = find_paths_reverse(servers, "dac", "svr", valid_nodes)
   paths_dac_fft = find_paths_reverse(servers, "fft", "dac", valid_nodes)
   paths_fft_out = find_paths_reverse(servers, "out", "fft", valid_nodes)
   
   # Count paths: svr -> fft -> dac -> out  
   paths_svr_fft = find_paths_reverse(servers, "fft", "svr", valid_nodes)
   paths_fft_dac = find_paths_reverse(servers, "dac", "fft", valid_nodes)
   paths_dac_out = find_paths_reverse(servers, "out", "dac", valid_nodes)
   
   # Total (note: this overcounts if paths share intermediate nodes, but for DAG it's often okay)
   total_order1 = paths_svr_dac * paths_dac_fft * paths_fft_out
   total_order2 = paths_svr_fft * paths_fft_dac * paths_dac_out
   
   print(f"Total paths through both dac and fft: {total_order1 + total_order2}")

main()
