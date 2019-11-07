import 'cross-fetch/polyfill';
import ApolloClient, { gql } from 'apollo-boost';
// import { ApolloQueryResult } from 'apollo-client';

import posts from './_posts';
import { Request, Response } from 'express';

export interface PostResult {
    body: string;
    date: string;
    modifiedTime: number;
    name: string;
    slug: string;
    tags: string[];
}

interface BlogPostQueryResults {
	listBlogPosts: {
		items: PostResult[]
	}
}

export const client = new ApolloClient({
    uri: 'https://glnjxdb4w5d2ljeb4wdiyymhre.appsync-api.us-east-1.amazonaws.com/graphql',
    headers: {
        "x-api-key": "da2-42tbnw3xw5es7kmpc7cgnpljpe"
    }
});

export const BLOG_POSTS = gql`
  {
    listBlogPosts {
		items {
		  body
		  date
		  modifiedTime
		  name
		  slug
		  tags
		}
	  }
  }
`;


// client.query({query: BLOG_POSTS})
//     .then((bposts: ApolloQueryResult<BlogPostQueryResults>) => {
//         console.log(bposts.data.listBlogPosts.items);
//     })

const contents = JSON.stringify(posts.map(post => {
    return {
        title: post.title,
        slug: post.slug
    };
}));

export function get(req: Request, res: Response) {
    res.writeHead(200, {
        'Content-Type': 'application/json'
    });

    res.end(contents);
}