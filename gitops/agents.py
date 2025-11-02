from typing import Optional, List, Dict
import os
from git import Repo
from git.exc import GitCommandError


class GitOperationsAgent:
    """
    A comprehensive Git repository management and version control operations agent.
    Provides high-level abstractions for common git operations with intelligent
    handling of branches, conflicts, and errors.
    """

    def __init__(self, repo_path: Optional[str] = None):
        """
        Initialize the Git Operations Agent.

        Args:
            repo_path: Optional path to an existing repository. 
                       If None, uses the current working directory.
        """
        self.repo_path = os.path.abspath(repo_path or os.getcwd())
        self.repo: Optional[Repo] = None

        git_dir = os.path.join(self.repo_path, ".git")
        if os.path.exists(git_dir):
            try:
                self.repo = Repo(self.repo_path)
            except Exception as e:
                raise Exception(f"Failed to initialize repository: {str(e)}") from e

    # ------------------------------------------------------------------
    def clone_repository(
        self, url: str, branch: Optional[str] = None, destination: Optional[str] = None
    ) -> Repo:
        """
        Clone a repository with optional branch targeting.

        Args:
            url: Repository URL to clone from
            branch: Optional specific branch to clone
            destination: Optional destination path

        Returns:
            git.Repo object representing the cloned repository
        """
        try:
            clone_path = os.path.abspath(destination or self.repo_path)
            kwargs = {"branch": branch} if branch else {}
            self.repo = Repo.clone_from(url, clone_path, **kwargs)
            return self.repo
        except GitCommandError as e:
            raise Exception(f"Failed to clone repository: {str(e)}") from e

    # ------------------------------------------------------------------
    def create_unique_branch(self, base_name: str, from_branch: str = "main") -> str:
        """
        Generate and create a unique branch name with collision avoidance.

        Args:
            base_name: Base name for the branch
            from_branch: Branch to create from

        Returns:
            Name of the created branch
        """
        if not self.repo:
            raise Exception("No repository initialized")

        counter = 1
        new_branch_name = base_name
        existing_branches = [b.name for b in self.repo.heads]

        while new_branch_name in existing_branches:
            new_branch_name = f"{base_name}-{counter}"
            counter += 1

        try:
            current_branch = self.repo.active_branch
            self.repo.git.checkout(from_branch)
            new_branch = self.repo.create_head(new_branch_name)
            new_branch.checkout()
            return new_branch_name
        except GitCommandError as e:
            self.repo.git.checkout(current_branch)
            raise Exception(f"Failed to create branch: {str(e)}") from e

    # ------------------------------------------------------------------
    def commit_changes(self, message: str, files: Optional[List[str]] = None) -> str:
        """
        Stage and commit modifications with automated handling.

        Args:
            message: Commit message
            files: Optional list of specific files to commit

        Returns:
            SHA of the new commit
        """
        if not self.repo:
            raise Exception("No repository initialized")

        try:
            if files:
                self.repo.index.add(files)
            else:
                self.repo.git.add(A=True)

            commit = self.repo.index.commit(message)
            return commit.hexsha
        except GitCommandError as e:
            raise Exception(f"Failed to commit changes: {str(e)}") from e

    # ------------------------------------------------------------------
    def push_branch(
        self, branch_name: Optional[str] = None, remote_name: str = "origin"
    ) -> bool:
        """
        Push changes with upstream configuration and conflict handling.

        Args:
            branch_name: Optional branch name to push
            remote_name: Name of the remote to push to

        Returns:
            True if push was successful
        """
        if not self.repo:
            raise Exception("No repository initialized")

        try:
            branch_name = branch_name or self.repo.active_branch.name
            remote = self.repo.remote(name=remote_name)
            remote.push(refspec=f"{branch_name}:{branch_name}", set_upstream=True)
            return True
        except GitCommandError as e:
            raise Exception(f"Failed to push branch: {str(e)}") from e

    # ------------------------------------------------------------------
    def get_repository_status(self) -> Dict:
        """
        Get comprehensive git status analysis.

        Returns:
            Dictionary containing repository status information
        """
        if not self.repo:
            raise Exception("No repository initialized")

        try:
            return {
                "current_branch": self.repo.active_branch.name if not self.repo.head.is_detached else "DETACHED_HEAD",
                "is_dirty": self.repo.is_dirty(),
                "untracked_files": self.repo.untracked_files,
                "modified_files": [item.a_path for item in self.repo.index.diff(None)],
                "staged_files": [item.a_path for item in self.repo.index.diff("HEAD")],
                "remotes": [remote.name for remote in self.repo.remotes],
                "branches": [branch.name for branch in self.repo.heads],
            }
        except GitCommandError as e:
            raise Exception(f"Failed to get repository status: {str(e)}") from e
