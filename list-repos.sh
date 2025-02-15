#!/bin/bash

username="standardgalactic"
repos=()

# Function to add unique repos to the list
add_unique_repos() {
	  local repo_names=("$@")
	    for repo in "${repo_names[@]}"; do
		        if [[ ! " ${repos[@]} " =~ " ${repo} " ]]; then
				      repos+=("$repo")
				          fi
					    done
				    }

			    echo "Fetching repositories the user has contributed to via their events..."
			    page=1
			    while : ; do
				      response=$(gh api -H "Accept: application/vnd.github+json" "/users/$username/events?page=$page&per_page=100")

				        if [[ -z "$response" ]]; then
						    break
						      fi

						        repo_names=$(echo "$response" | jq -r '.[] | select(.type == "PushEvent" or .type == "PullRequestEvent") | .repo.name')

							  if [[ -z "$repo_names" ]]; then
								      break
								        fi

									  add_unique_repos $repo_names
									    ((page++))
								    done

								    echo "Fetching repositories the user has starred..."
								    page=1
								    while : ; do
									      response=$(gh api -H "Accept: application/vnd.github+json" "/users/$username/starred?page=$page&per_page=100")

									        if [[ -z "$response" ]]; then
											    break
											      fi

											        repo_names=$(echo "$response" | jq -r '.[].full_name')

												  if [[ -z "$repo_names" ]]; then
													      break
													        fi

														  add_unique_repos $repo_names
														    ((page++))
													    done

													    echo "Fetching repositories the user owns..."
													    page=1
													    while : ; do
														      response=$(gh api -H "Accept: application/vnd.github+json" "/users/$username/repos?page=$page&per_page=100")

														        if [[ -z "$response" ]]; then
																    break
																      fi

																        repo_names=$(echo "$response" | jq -r '.[].full_name')

																	  if [[ -z "$repo_names" ]]; then
																		      break
																		        fi

																			  add_unique_repos $repo_names
																			    ((page++))
																		    done

																		    # Remove duplicates and sort the repositories
																		    echo "Removing duplicates and sorting repositories..."
																		    unique_repos=($(echo "${repos[@]}" | tr ' ' '\n' | sort -u))

																		    echo "Repositories:"
																		    for repo in "${unique_repos[@]}"; do
																			      echo "$repo"
																		      done

																		      echo "Done!"

